import os
# Must be set BEFORE importing numpy/pandas/gamspy
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import time
import shutil
import tempfile
import atexit
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import pandas as pd

from gamspy_model.meshr_class import ReactiveDistillationModel
from functions.exhuaustive_comb import generate_scenarios_optimized

_WORKER_MODEL = None
_WORKER_DIR = None


def _cleanup_worker():
    global _WORKER_MODEL, _WORKER_DIR
    if _WORKER_MODEL is not None:
        try:
            _WORKER_MODEL.m.close()
        except Exception:
            pass
    if _WORKER_DIR is not None:
        shutil.rmtree(_WORKER_DIR, ignore_errors=True)


def init_worker(max_stages=22):
    global _WORKER_MODEL, _WORKER_DIR
    _WORKER_DIR = tempfile.mkdtemp(prefix=f"gams_w{os.getpid()}_")
    _WORKER_MODEL = ReactiveDistillationModel(max_stages=max_stages, working_directory=_WORKER_DIR)
    atexit.register(_cleanup_worker)


def count_contiguous_sections(stages):
    if not stages:
        return 0
    s = sorted(stages)
    return 1 + sum(1 for a, b in zip(s, s[1:]) if b - a > 1)


def solve_scenario(config, solver_name="BARON"):
    meshr = _WORKER_MODEL

    Ns = config["Ns"]
    NFE = config["NFE"]
    NFB = config["NFB"]
    reactive = sorted(config["reactive"])

    meshr.reset_levels()
    meshr.update_config(Ns=Ns, NFE=NFE, NFB=NFB, reactive_trays=reactive)

    # Fast CONOPT warm-start before BARON
    conopt_time = 0.0
    if solver_name.upper() == "BARON":
        ws = meshr.solve(solver="CONOPT", threads=1, time_limit=15)
        conopt_time = float(meshr.model.solve_model_time) if meshr.flag_solver else 0.0
        # If CONOPT diverged, reset levels so BARON starts cleanly
        if getattr(ws["Status"], "value", -1) not in (1, 2):
            meshr.reset_levels()
            meshr._init_temp_and_hr()

    result = meshr.solve(solver=solver_name, threads=1, time_limit=160)

    status = result["Status"]
    status_code = getattr(status, "value", -1)
    solved_ok = status_code in (1, 2)

    rec = {
        "Ns": Ns,
        "N_int": Ns - 2,
        "NFE": NFE,
        "NFB": NFB,
        "NR1": reactive[0] if len(reactive) > 0 else np.nan,
        "NR2": reactive[1] if len(reactive) > 1 else np.nan,
        "NR3": reactive[2] if len(reactive) > 2 else np.nan,
        "N_rect": NFE - 2,
        "N_strip": (Ns - 1) - NFB,
        "N_rxn_sections": count_contiguous_sections(reactive),
        "Status": str(status),
        "Status_Code": status_code,
        "WarmStart_Time_s": conopt_time,
        "Solve_Time_s": float(meshr.model.solve_model_time) if meshr.flag_solver else 0.0,
        "Total_Time_s": float(meshr.model.total_solve_time) if meshr.flag_solver else 0.0,
        "Profit": result["Profit"] if solved_ok else np.nan,
        "TAC_yr": result["Profit"] * 1e6 if solved_ok else np.nan,
    }

    if not solved_ok:
        return rec

    j_act = [str(s) for s in range(1, Ns + 1)]
    j_int = [str(s) for s in range(2, Ns)]
    j_rxn = [str(s) for s in reactive]

    L_s   = meshr.L.records.set_index("j").loc[j_act, "level"].values * meshr.F_factor
    T_s   = meshr.T.records.set_index("j").loc[j_act, "level"].values
    x_df  = meshr.x.records.pivot(index="i", columns="j", values="level")
    rxn_r = meshr.Rxn_Rate.records.set_index("j").loc[j_rxn, "level"].values * meshr.m_cat

    FE_val   = meshr.FE.toValue() * meshr.F_factor
    FB_val   = meshr.FB.toValue() * meshr.F_factor
    D_val    = meshr.D.toValue() * meshr.F_factor
    Breb_val = meshr.Breb.toValue() * meshr.F_factor
    Qr_Jmin  = meshr.Qr.toValue() * meshr.FH_factor
    Qc_Jmin  = meshr.Qc.toValue() * meshr.FH_factor
    Dcol_val = meshr.Dcol.toValue()
    ht_val   = meshr.ht.toValue()

    AF_val    = getattr(meshr, "AF", 1.0 / 3.0)
    SF_val    = getattr(meshr, "SF", 0.15)
    hours_yr  = getattr(meshr, "hours_yr", 8000.0)
    c_steam_v = meshr.c_steam.toValue()
    c_cw_v    = meshr.c_cw.toValue() if hasattr(meshr, "c_cw") else 0.378e-9
    c_cat_v   = meshr.C_cat.toValue() if hasattr(meshr, "C_cat") else 7.7

    shell_c = meshr.v_ColCost.toValue() * AF_val
    tray_c  = meshr.v_TrayCost.toValue() * AF_val
    cond_c  = meshr.v_CondCost.toValue() * AF_val
    reb_c   = meshr.v_RebCost.toValue() * AF_val
    cat_c   = c_cat_v * len(reactive) * meshr.m_cat * AF_val
    capex   = meshr.CAP_cost.toValue()

    steam_c = c_steam_v * Qr_Jmin * hours_yr * 60.0
    cw_c    = c_cw_v * Qc_Jmin * hours_yr * 60.0
    feed_c  = (FE_val * meshr.CostEth.toValue() + FB_val * meshr.CostBut.toValue()) * hours_yr * 60.0
    rev_c   = Breb_val * meshr.CostETBE.toValue() * hours_yr * 60.0
    op_net  = meshr.OP_cost.toValue()

    IB_in = FB_val * 0.3
    X_IB = (IB_in - (Breb_val * x_df.loc["3", str(Ns)] + D_val * x_df.loc["3", "1"])) / IB_in
    H_shell = (1.0 + SF_val) * ht_val * (Ns - 2)
    uf_s  = meshr.uf.records.set_index("j").loc[j_int, "level"].values
    ufl_s = meshr.ufl.records.set_index("j").loc[j_int, "level"].values
    flood_pct = 100.0 * uf_s / ufl_s
    V_cat_req = meshr.m_cat / meshr.rho_cat.toValue()
    V_cat_av  = meshr.phi_c.toValue() * (np.pi / 4.0) * (Dcol_val**2) * meshr.h_pack.toValue()
    T_rxn = [T_s[r - 1] for r in reactive]
    x_etoh_rxn = [x_df.loc["2", str(r)] for r in reactive]

    rec.update({
        "Dcol": Dcol_val,
        "LD_ratio": H_shell / Dcol_val,
        "RR": L_s[0] / D_val,
        "FE_molmin": FE_val,
        "D_molmin": D_val,
        "Breb_molmin": Breb_val,
        "Qr_kJmin": Qr_Jmin / 1e3,
        "Qc_kJmin": Qc_Jmin / 1e3,
        "Tcond_K": meshr.Tcond.toValue(),
        "Treb_K": meshr.Treb.toValue(),
        "X_IB": X_IB,
        "x_EtOH_top": x_df.loc["2", "1"],
        "x_EtOH_bot": x_df.loc["2", str(Ns)],
        "Flood_min_pct": float(flood_pct.min()),
        "Flood_max_pct": float(flood_pct.max()),
        "Cat_fill_pct": 100.0 * V_cat_req / V_cat_av,
        "Rxn_min_xEtOH": float(min(x_etoh_rxn)),
        "Rxn_max_T_K": float(max(T_rxn)),
        "Rxn_min_rate": float(rxn_r.min()),
        "Rxn_total_rate": float(rxn_r.sum()),
        "CAPEX": capex,
        "Shell_Cost": shell_c,
        "Tray_Cost": tray_c,
        "Cond_Cost": cond_c,
        "Reb_Cost": reb_c,
        "Cat_Cost": cat_c,
        "OPEX_gross": feed_c + steam_c + cw_c,
        "Feed_Cost": feed_c,
        "Steam_Cost": steam_c,
        "CW_Cost": cw_c,
        "ETBE_Rev": rev_c,
        "OPEX_net": op_net,
    })
    return rec


if __name__ == "__main__":
    Nsmax = 14
    NRx = 3
    SOLVER = "BARON"
    MAX_WORKERS = 10
    FLUSH_EVERY = 100

    os.makedirs("result", exist_ok=True)
    ex_txt = f"exhaustive_{NRx+3}D"
    csv_path = os.path.join("result", ex_txt + ".csv")
    txt_path = os.path.join("result", ex_txt + ".txt")

    all_scenarios = generate_scenarios_optimized(Nsmax, NRx)

    # Resume support: load already-completed discrete keys if CSV exists
    done_keys = set()
    file_exists = os.path.isfile(csv_path) and os.path.getsize(csv_path) > 0
    if file_exists:
        prev_df = pd.read_csv(csv_path, sep=";")
        for r in prev_df[["Ns", "NFE", "NFB", "NR1", "NR2", "NR3"]].itertuples(index=False):
            done_keys.add(tuple(int(x) for x in r))
        print(f"Resuming: {len(done_keys)}/{len(all_scenarios)} already completed.", flush=True)

    pending = [
        cfg for cfg in all_scenarios
        if (cfg["Ns"], cfg["NFE"], cfg["NFB"], *sorted(cfg["reactive"])) not in done_keys
    ]
    print(f"Running {len(pending)} pending scenarios on {MAX_WORKERS} workers...", flush=True)

    start_time = time.perf_counter()
    buffer = []
    completed_now = 0

    if pending:
        with ProcessPoolExecutor(max_workers=MAX_WORKERS, initializer=init_worker, initargs=(22,)) as executor:
            futures = {executor.submit(solve_scenario, cfg, SOLVER): cfg for cfg in pending}
            for fut in as_completed(futures):
                cfg = futures[fut]
                try:
                    res = fut.result()
                except Exception as e:
                    r = sorted(cfg["reactive"])
                    res = {
                        "Ns": cfg["Ns"], "NFE": cfg["NFE"], "NFB": cfg["NFB"],
                        "NR1": r[0], "NR2": r[1], "NR3": r[2],
                        "Status": f"Crash:{e}", "Status_Code": -99, "Profit": np.nan,
                    }
                buffer.append(res)
                completed_now += 1

                if len(buffer) >= FLUSH_EVERY or completed_now == len(pending):
                    pd.DataFrame(buffer).to_csv(
                        csv_path, mode="a", header=not file_exists, index=False, sep=";"
                    )
                    file_exists = True
                    buffer.clear()
                    elapsed = time.perf_counter() - start_time
                    rate = completed_now / max(elapsed, 1e-6)
                    eta_min = (len(pending) - completed_now) / max(rate, 1e-6) / 60.0
                    total_done = len(done_keys) + completed_now
                    print(
                        f"[{total_done:5d}/{len(all_scenarios)}] "
                        f"({100*total_done/len(all_scenarios):5.1f}%) | "
                        f"Rate: {rate:.2f} cfg/s | ETA: {eta_min:.1f} min",
                        flush=True,
                    )

    elapsed_time = time.perf_counter() - start_time

    # Final sort & summary across all completed rows
    df = pd.read_csv(csv_path, sep=";").sort_values("Profit", na_position="last")
    df.to_csv(csv_path, index=False, sep=";")

    total_comb = len(all_scenarios)
    solved_space = int(df["Profit"].notna().sum())
    solved_space_perc = solved_space / total_comb * 100.0
    mean_solve_s = df.loc[df["Profit"].notna(), "Solve_Time_s"].mean()
    status_counts = df["Status"].value_counts().to_dict()

    with open(txt_path, "a") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Run date: {datetime.now()}\n")
        f.write(f"Solver: {SOLVER} (workers={MAX_WORKERS})\n")
        f.write(f"Wall-clock time (this session): {elapsed_time:.2f} s | Mean BARON solve time: {mean_solve_s:.3f} s\n")
        f.write(f"Nsmax: {Nsmax} | NRx: {NRx}\n")
        f.write(f"Total combinatory space: {total_comb}\n")
        f.write(f"Solved candidates: {solved_space} ({solved_space_perc:.2f}%)\n")
        f.write(f"Status counts: {status_counts}\n")
        if solved_space > 0:
            best_sol = df.iloc[0]
            f.write("Minimum Objective Value and design variables:\n")
            f.write("; ".join(f"{col}={best_sol[col]}" for col in df.columns) + "\n")