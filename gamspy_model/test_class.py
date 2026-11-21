# testing the class
from meshr_class import ReactiveDistillationModel
import numpy as np
import pickle
# from meshr_class_without_cat_res import ReactiveDistillationModel

# 1. Initialize the class (Builds the 22-stage matrix once)
meshr = ReactiveDistillationModel(max_stages=22)

# 2. Define the different column configurations you want to test
scenarios = [
    # {"Ns": 7, "NFE": 4, "NFB": 4, "reactive": [4]},            # 1 reactive tray, taller column
    # {"Ns": 8, "NFE": 4, "NFB": 5, "reactive": [3, 5]},          # 2 reactive trays, even taller
    # {"Ns": 9, "NFE": 5, "NFB": 6, "reactive": [3, 5, 6]},      # 3 reactive trays
    # {"Ns": 10, "NFE": 3, "NFB": 8, "reactive": [4, 5, 6]},      # 3 reactive trays
    {"Ns": 18, "NFE": 6, "NFB": 15, "reactive": [6, 11, 15]}  # Linan et al. (2020) best 3-section optimum,

]
# [10, 5, 7, 3, 5, 6, 7]
# [10, 5, 7, 3, 5, 6, 7]
# Ns  = 10
# NFE = 5
# NFB = 7
# NR1 = 3
# NR2 = 5
# NR3 = 7

all_scenarios_data = []

for config in scenarios:
    meshr.update_config(
        Ns=config["Ns"],
        NFE=config["NFE"],
        NFB=config["NFB"],
        reactive_trays=config["reactive"]
    )

    result = meshr.solve(solver="CONOPT", dataframe=True, export=True)
    status = result["Status"]
    print(f"Result: {status} | Obj (1e6 $/yr): {result['Profit']}")

    # 0. Guard against failed/infeasible solves
    if status == "fail" or getattr(status, "value", -1) not in (1, 2):
        print("  >>> SKIPPING DIAGNOSTICS: Solver did not converge to an optimal solution.")
        all_scenarios_data.append({"config": config, "solver_status": status, "profit": result["Profit"]})
        continue

    Ns = config["Ns"]
    j_act = [str(s) for s in range(1, Ns + 1)]
    j_int = [str(s) for s in range(2, Ns)]

    # --- Safe extraction indexed by stage number ---
    L_s   = meshr.L.records.set_index("j").loc[j_act, "level"].values * meshr.F_factor
    V_s   = meshr.V.records.set_index("j").loc[j_act, "level"].values * meshr.F_factor
    T_s   = meshr.T.records.set_index("j").loc[j_act, "level"].values
    x_mat = meshr.x.records.pivot(index="i", columns="j", values="level").loc[["1", "2", "3", "4"], j_act].values
    y_mat = meshr.y.records.pivot(index="i", columns="j", values="level").loc[["1", "2", "3", "4"], j_act].values
    rxn_s = meshr.Rxn_Rate.records.set_index("j").loc[j_act, "level"].values  # mol/(kg_cat*min)

    FE_val   = meshr.FE.toValue() * meshr.F_factor
    FB_val   = meshr.FB.toValue() * meshr.F_factor
    D_val    = meshr.D.toValue() * meshr.F_factor
    Breb_val = meshr.Breb.toValue() * meshr.F_factor
    Qr_Jmin  = meshr.Qr.toValue() * meshr.FH_factor
    Qc_Jmin  = meshr.Qc.toValue() * meshr.FH_factor
    Dcol_val = meshr.Dcol.toValue()
    ht_val   = meshr.ht.toValue()
    Tcond_v  = meshr.Tcond.toValue()
    Treb_v   = meshr.Treb.toValue()

    # Dynamic model parameters (stays synced with meshr_class.py)
    AF_val    = getattr(meshr, "AF", 1.0 / 3.0)
    SF_val    = getattr(meshr, "SF", 0.15)
    hours_yr  = getattr(meshr, "hours_yr", 8000.0)
    c_steam_v = meshr.c_steam.toValue()
    c_cw_v    = meshr.c_cw.toValue() if hasattr(meshr, "c_cw") else 0.378e-9
    c_cat_v   = meshr.C_cat.toValue() if hasattr(meshr, "C_cat") else 7.7
    n_rx      = int(np.sum(meshr.is_reactive.records["value"].values))

    # --- 1. PROCESS, REACTION & DIMERIZATION CHECK ---
    RR = L_s[0] / D_val
    IB_in = FB_val * 0.3
    IB_reacted = IB_in - (Breb_val * x_mat[2, -1] + D_val * x_mat[2, 0])
    X_IB = IB_reacted / IB_in
    etoh_ib_feed = FE_val / IB_in
    etoh_ib_rxn  = FE_val / max(IB_reacted, 1e-12)
    total_rxn    = np.sum(meshr.m_cat * rxn_s)
    mol_bal_err  = (FE_val + FB_val) - (D_val + Breb_val) - total_rxn

    print("\n" + "=" * 78)
    print(f"CONFIG: Ns={Ns} (N_int={Ns-2}) | NFE={config['NFE']} | NFB={config['NFB']} | Rxn={config['reactive']}")
    print("=" * 78)
    print("[1] PROCESS, REACTION & DIMERIZATION SAFETY")
    print(f"  Reflux Ratio (RR)         : {RR:.3f}")
    print(f"  FE / FB (mol/min)         : {FE_val:.4f} / {FB_val:.4f}  (EtOH/IB_in={etoh_ib_feed:.3f}, EtOH/IB_rxn={etoh_ib_rxn:.3f})")
    print(f"  D / Breb (mol/min)        : {D_val:.4f} / {Breb_val:.4f}  (Mole bal err = {mol_bal_err:.2e})")
    print(f"  IB Conversion (X_IB)      : {X_IB*100:.2f}%  |  Bottoms ETBE x4 = {x_mat[3, -1]:.4f}")
    print(f"  EtOH Distillate / Bottoms : x2[1]={x_mat[1, 0]:.4f} ({D_val*x_mat[1,0]:.4f} mol/min) | x2[Ns]={x_mat[1, -1]:.4f} ({Breb_val*x_mat[1,-1]:.4f} mol/min)")

    # --- 2. THERMAL & EXCHANGER SANITY ---
    lmtd_c = 10.0 / np.log((Tcond_v - 303.15) / (Tcond_v - 313.15))
    U_c = 150.0 / 0.17611
    U_r = 170.0 / 0.17611 if hasattr(meshr, "F_BM_reb") else 250.0 / 0.17611
    A_cond_m2 = (Qc_Jmin / 60.0) / (U_c * lmtd_c)
    A_reb_m2  = (Qr_Jmin / 60.0) / (U_r * (433.15 - Treb_v))

    print("\n[2] THERMAL & HEAT EXCHANGERS")
    print(f"  Qr = {Qr_Jmin/1e3:7.2f} kJ/min ({Qr_Jmin/6e4:5.2f} kW) | Treb  = {Treb_v:.2f} K (dT_stm={433.15-Treb_v:4.1f} K) | A_reb  = {A_reb_m2:.4f} m2")
    print(f"  Qc = {Qc_Jmin/1e3:7.2f} kJ/min ({Qc_Jmin/6e4:5.2f} kW) | Tcond = {Tcond_v:.2f} K (LMTD  ={lmtd_c:4.1f} K) | A_cond = {A_cond_m2:.4f} m2")

    # --- 3. HYDRAULICS & GEOMETRY ---
    H_shell   = (1.0 + SF_val) * ht_val * (Ns - 2)
    LD_ratio  = H_shell / Dcol_val
    uf_s      = meshr.uf.records.set_index("j").loc[j_int, "level"].values
    ufl_s     = meshr.ufl.records.set_index("j").loc[j_int, "level"].values
    flv_s     = meshr.Flv.records.set_index("j").loc[j_int, "level"].values
    flood_pct = 100.0 * uf_s / ufl_s
    V_cat_req = meshr.m_cat / meshr.rho_cat.toValue()
    V_cat_av  = meshr.phi_c.toValue() * (np.pi / 4) * Dcol_val**2 * meshr.h_pack.toValue()
    cat_marg  = meshr.def_catal_vol.records["marginal"].values[0]
    ld_marg   = meshr.eq_LD_ratio.records["marginal"].values[0] if hasattr(meshr, "eq_LD_ratio") else 0.0

    print("\n[3] HYDRAULICS & GEOMETRY")
    print(f"  Dcol = {Dcol_val:.4f} m | ht = {ht_val*39.3701:.1f} in | H_shell = {H_shell:.2f} m | L/D = {LD_ratio:.2f} (marg={ld_marg:.2e})")
    print(f"  Flooding % (min / max)    : {flood_pct.min():.1f}% / {flood_pct.max():.1f}%  (limits: 15% - 80%)")
    
    print(f"  Flv (min / max)           : {flv_s.min():.4f} / {flv_s.max():.4f}  (bounds: 0.02 - 1.00)")
    print(f"  Catalyst vol used/avail   : {V_cat_req*1e6:.1f} / {V_cat_av*1e6:.1f} cm3 (fill={100*V_cat_req/V_cat_av:.1f}%, marg={cat_marg:.2e})")

    # --- 4. ECONOMICS & EXACT RECONCILIATION (1990s basis) ---
    ColCost  = meshr.v_ColCost.toValue()  * AF_val
    TrayCost = meshr.v_TrayCost.toValue() * AF_val
    CondCost = meshr.v_CondCost.toValue() * AF_val
    RebCost  = meshr.v_RebCost.toValue()  * AF_val
    cat_cost = c_cat_v * n_rx * meshr.m_cat * AF_val
    cap_cost = meshr.CAP_cost.toValue()
    cap_err  = (ColCost + TrayCost + CondCost + RebCost + cat_cost) - cap_cost

    steam_cost   = c_steam_v * Qr_Jmin * hours_yr * 60.0
    cooling_cost = c_cw_v    * Qc_Jmin * hours_yr * 60.0
    raw_products = (FE_val * meshr.CostEth.toValue() + FB_val * meshr.CostBut.toValue()) * hours_yr * 60.0
    revenue      = Breb_val * meshr.CostETBE.toValue() * hours_yr * 60.0
    gross_opex   = raw_products + steam_cost + cooling_cost
    op_cost      = meshr.OP_cost.toValue()
    op_err       = (gross_opex - revenue) - op_cost

    print(f"\n[4] ECONOMICS ($/yr | AF={AF_val:.4f}, {hours_yr:.0f} h/yr)")
    print(f"  Annualized CAPEX          : ${cap_cost:,.2f}/yr  (check err = {cap_err:+.2e})")
    print(f"    Shell=${ColCost:,.1f} | Trays=${TrayCost:,.1f} | Cond=${CondCost:,.1f} | Reb=${RebCost:,.1f} | Cat=${cat_cost:,.2f}")
    print(f"  Gross Operating Cost      : ${gross_opex:,.2f}/yr  (Feeds=${raw_products:,.1f} | Steam=${steam_cost:,.1f} | CW=${cooling_cost:,.1f})")
    print(f"  ETBE Revenue              : ${revenue:,.2f}/yr")
    print(f"  Net OPEX (Gross - Rev)    : ${op_cost:,.2f}/yr  (check err = {op_err:+.2e})")
    print(f"  TOTAL ANNUAL COST (Obj)   : ${cap_cost + op_cost:,.2f}/yr  (model obj*1e6 = ${meshr.obj.toValue()*1e6:,.2f}/yr)")

    # --- 5. COMPACT STAGE-BY-STAGE PROFILE ---
    print("\n[5] STAGE PROFILE (flags: * = Rxn, E = EtOH feed, B = Butenes feed, ! = low EtOH or T>393K)")
    print("  Stg Tag |  T (K)  |  L (m/m) |  V (m/m) | x_EtOH  x_IB  x_ETBE | Flood%   Flv  | Rxn (mol/m)")
    print("  " + "-" * 90)
    for idx in range(Ns):
        s = idx + 1
        tag = ("*" if s in config["reactive"] else " ") + ("E" if s == config["NFE"] else " ") + ("B" if s == config["NFB"] else " ")
        if s == 1 or s == Ns:
            fl_str, flv_str = "   -  ", "   -  "
        else:
            fl_val = flood_pct[idx - 1]
            fl_mark = "L" if fl_val <= 15.05 else ("H" if fl_val >= 79.95 else " ")
            fl_str  = f"{fl_val:5.1f}{fl_mark}"
            flv_str = f"{flv_s[idx - 1]:6.3f}"
            # fl_mark = "L" if fl_val <= 15.05 else ("H" if fl_val >= 79.95 else " ")
        warn = ""
        if s in config["reactive"]:
            if T_s[idx] > 393.15: warn += " !T>120C"
            if x_mat[1, idx] < 0.04: warn += " !lowEtOH"
            if rxn_s[idx] < 0: warn += " !revRxn"
        print(f"  {s:3d} {tag} | {T_s[idx]:7.2f} | {L_s[idx]:8.3f} | {V_s[idx]:8.3f} | "
              f"{x_mat[1,idx]:6.3f} {x_mat[2,idx]:6.3f} {x_mat[3,idx]:6.3f} | {fl_str} {flv_str} | {meshr.m_cat*rxn_s[idx]:+8.4f}{warn}")

    # --- 6. ACTIVE BOUNDS CHECK ---
    bound_hits = []
    for vname in ["FE", "D", "Breb", "Qc", "Qr", "Dcol", "Tcond", "Treb"]:
        rec = getattr(meshr, vname).records.iloc[0]
        if abs(rec["level"] - rec["lower"]) <= 1e-6 * max(1.0, abs(rec["lower"])):
            bound_hits.append(f"{vname} @ LO ({rec['lower']:.4g})")
        elif abs(rec["level"] - rec["upper"]) <= 1e-6 * max(1.0, abs(rec["upper"])):
            bound_hits.append(f"{vname} @ UP ({rec['upper']:.4g})")
    for vname in ["T", "L", "V", "Flv", "CF", "Rxn_Rate"]:
        rec = getattr(meshr, vname).records.set_index("j").loc[j_int]
        lo_hits = rec.index[(rec["level"] - rec["lower"]).abs() <= 1e-6 * rec["lower"].abs().clip(lower=1.0)].tolist()
        up_hits = rec.index[(rec["upper"] - rec["level"]).abs() <= 1e-6 * rec["upper"].abs().clip(lower=1.0)].tolist()
        if lo_hits: bound_hits.append(f"{vname}[{','.join(lo_hits)}] @ LO")
        if up_hits: bound_hits.append(f"{vname}[{','.join(up_hits)}] @ UP")
    print("\n[6] ACTIVE VARIABLE BOUNDS:", ", ".join(bound_hits) if bound_hits else "None (interior optimum)")

    # --- Store cleanly synced results ---
    scenario_dict = {
        "config": config,
        "solver_status": status,
        "profit": result["Profit"],
        "metrics": {
            "Qr": Qr_Jmin, "Qc": Qc_Jmin, "FE": FE_val, "FB": FB_val, "Dcol": Dcol_val,
            "Breb": Breb_val, "D": D_val, "X_IB": X_IB, "RR": RR, "Tcond": Tcond_v,
            "Treb": Treb_v, "ColCost": ColCost, "TrayCost": TrayCost,
            "CondCost": CondCost, "RebCost": RebCost, "n_rx": n_rx,
            "cat_cost": cat_cost, "cap_cost": cap_cost, "steam_cost": steam_cost,
            "cooling_cost": cooling_cost, "raw_products": raw_products,
            "gross_opex": gross_opex, "op_cost": op_cost, "revenue": revenue,
            "LD_ratio": LD_ratio, "flood_min": flood_pct.min(), "flood_max": flood_pct.max(),
        },
        "profiles": {
            "L": L_s, "V": V_s, "x": x_mat, "y": y_mat, "T": T_s,
            "rxn": meshr.m_cat * rxn_s, "flood_pct": flood_pct, "Flv": flv_s,
        },
    }
    all_scenarios_data.append(scenario_dict)

# Save to file
with open("meshr_results.pkl", "wb") as f:
    pickle.dump(all_scenarios_data, f)
    





