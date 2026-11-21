import os
# Must come BEFORE importing numpy, pandas, or gamspy
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import time
import atexit
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import pandas as pd

from gamspy_model.meshr_class import ReactiveDistillationModel
from functions.exhuaustive_comb import generate_scenarios_optimized

_WORKER_MODEL = None


def init_worker(max_stages=22):
    global _WORKER_MODEL
    _WORKER_MODEL = ReactiveDistillationModel(max_stages=max_stages)
    atexit.register(_WORKER_MODEL.m.close)


def solve_one(config):
    meshr = _WORKER_MODEL
    Ns = config["Ns"]
    NFE = config["NFE"]
    NFB = config["NFB"]
    reactive = sorted(config["reactive"])

    # Clean starting point
    if hasattr(meshr, "reset_levels"):
        meshr.reset_levels()
    else:
        meshr._initialize_bounds_and_scales()

    meshr.update_config(Ns=Ns, NFE=NFE, NFB=NFB, reactive_trays=reactive)

    # 1. Fast CONOPT warm-start
    ws = meshr.solve(solver="CONOPT", time_limit=15)
    conopt_ok = getattr(ws["Status"], "value", -1) in (1, 2)
    conopt_profit = ws["Profit"] if conopt_ok else np.nan
    conopt_t = float(meshr.model.solve_model_time) if meshr.flag_solver else 0.0

    # Reset if CONOPT failed so BARON does not inherit a diverged point
    if not conopt_ok:
        if hasattr(meshr, "reset_levels"):
            meshr.reset_levels()
        else:
            meshr._initialize_bounds_and_scales()
        meshr._init_temp_and_hr()

    # 2. BARON global proof
    res = meshr.solve(solver="BARON", time_limit=160)
    status = res["Status"]
    status_code = getattr(status, "value", -1)
    solved_ok = status_code in (1, 2)
    profit = res["Profit"] if solved_ok else np.nan

    rec = {
        "Ns": Ns,
        "NFE": NFE,
        "NFB": NFB,
        "NR1": reactive[0],
        "NR2": reactive[1],
        "NR3": reactive[2],
        "CONOPT_Status": str(ws["Status"]),
        "CONOPT_Time_s": conopt_t,
        "BARON_Status": str(status),
        "BARON_Time_s": float(meshr.model.solve_model_time) if meshr.flag_solver else 0.0,
        "Profit": profit,
        "TAC_yr": profit * 1e6 if solved_ok else np.nan,
        "Global_minus_Local_yr": (profit - conopt_profit) * 1e6 if (solved_ok and np.isfinite(conopt_profit)) else np.nan,
        "FE_molmin": meshr.FE.toValue() * meshr.F_factor if solved_ok else np.nan,
        "Dcol": meshr.Dcol.toValue() if solved_ok else np.nan,
    }
    return rec


if __name__ == "__main__":
    Nsmax = 14
    NRx = 3
    N_SAMPLES = 20
    MAX_WORKERS = 4

    os.makedirs("result", exist_ok=True)
    csv_path = os.path.join("result", f"smoke_test_{NRx+3}D.csv")

    all_scenarios = generate_scenarios_optimized(Nsmax, NRx)
    step = max(1, len(all_scenarios) // N_SAMPLES)
    test_scenarios = all_scenarios[::step][:N_SAMPLES]

    print(f"Starting smoke test: {len(test_scenarios)} scenarios (sampled from {len(all_scenarios)}) on {MAX_WORKERS} workers...\n", flush=True)
    t_start = time.perf_counter()
    results = []

    with ProcessPoolExecutor(max_workers=MAX_WORKERS, initializer=init_worker, initargs=(22,)) as executor:
        futures = {executor.submit(solve_one, cfg): cfg for cfg in test_scenarios}
        for idx, fut in enumerate(as_completed(futures), start=1):
            cfg = futures[fut]
            try:
                rec = fut.result()
            except Exception as e:
                rec = {
                    "Ns": cfg["Ns"], "NFE": cfg["NFE"], "NFB": cfg["NFB"],
                    "NR1": cfg["reactive"][0], "NR2": cfg["reactive"][1], "NR3": cfg["reactive"][2],
                    "BARON_Status": f"Crash: {e}", "BARON_Time_s": np.nan, "Profit": np.nan, "TAC_yr": np.nan,
                }
            results.append(rec)
            tac_str = f"${rec['TAC_yr']:,.1f}/yr" if pd.notna(rec.get("TAC_yr")) else "N/A"
            print(
                f"[{idx:2d}/{len(test_scenarios)}] Ns={rec['Ns']:2d} NFE={rec['NFE']:2d} NFB={rec['NFB']:2d} "
                f"Rxn=[{rec['NR1']},{rec['NR2']},{rec['NR3']}] | "
                f"{rec['BARON_Status']:28s} | {rec['BARON_Time_s']:5.1f} s | TAC={tac_str}",
                flush=True,
            )

    elapsed = time.perf_counter() - t_start
    df = pd.DataFrame(results).sort_values("Profit", na_position="last")
    df.to_csv(csv_path, index=False, sep=";")

    n_ok = int(df["Profit"].notna().sum())
    print("\n" + "=" * 78)
    print(f"SMOKE TEST COMPLETE in {elapsed:.1f} s  |  Saved to: {csv_path}")
    print(f"Status counts    : {df['BARON_Status'].value_counts().to_dict()}")
    print(f"Solved           : {n_ok}/{len(test_scenarios)}")
    if n_ok > 0:
        print(f"Mean BARON time  : {df.loc[df['Profit'].notna(), 'BARON_Time_s'].mean():.2f} s (solved) | "
              f"{df['BARON_Time_s'].mean():.2f} s (all)")
        print(f"FE range         : {df['FE_molmin'].min():.4f} to {df['FE_molmin'].max():.4f} mol/min")
        best = df.iloc[0]
        print(f"Best found       : ${best['TAC_yr']:,.2f}/yr  (Ns={int(best['Ns'])}, NFE={int(best['NFE'])}, "
              f"NFB={int(best['NFB'])}, Rxn=[{int(best['NR1'])},{int(best['NR2'])},{int(best['NR3'])}])")
    print("=" * 78)