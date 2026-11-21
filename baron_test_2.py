import sys
import numpy as np
import gamspy as gp
from gamspy_model.meshr_class import ReactiveDistillationModel

CASES = [
    ("ANOMALY row 7 ", 14, 5, 11, [3, 8, 11]),
    ("ANOMALY row 22", 14, 6, 11, [5, 9, 11]),
    ("ANOMALY row 28", 14, 6, 11, [4, 9, 11]),
    ("NORMAL  row 3 ", 14, 5, 11, [3, 7, 11]),
]

BARON_OPTS = {
    "AllowExternal": 0,
    "AllowMinos": 0,
    "AllowSnopt": 0,
    "NumLoc": 1,
    "Threads": 1,
    "MaxTime": 160,
}

def inspect_condenser(meshr, tag):
    L_rec = meshr.L.records.set_index("j")
    V_rec = meshr.V.records.set_index("j")
    Hl_rec = meshr.Hl.records.set_index("j")
    Hv_rec = meshr.Hv.records.set_index("j")

    L1 = float(L_rec.loc["1", "level"])
    L2 = float(L_rec.loc["2", "level"])
    V1 = float(V_rec.loc["1", "level"])
    V2 = float(V_rec.loc["2", "level"])
    D  = float(meshr.D.toValue())
    Qc = float(meshr.Qc.toValue())
    Hl1 = float(Hl_rec.loc["1", "level"])
    Hv1 = float(Hv_rec.loc["1", "level"])
    Hv2 = float(Hv_rec.loc["2", "level"])

    mol_res = V1 + (L1 + D) - V2
    eng_res = V1 * Hv1 + (L1 + D) * Hl1 - V2 * Hv2 + Qc
    RR = L1 / D
    shell_scaled = (meshr.v_ColCost.toValue() * meshr.AF) / 1e6

    print(f"  [{tag}] Status={meshr.model.status} | Obj={meshr.obj.toValue():.8f}")
    print(f"    L['1']={L1:+.10f} (lo={L_rec.loc['1','lower']}) | L['2']={L2:+.6f} | D={D:.6f} | RR={RR:+.6f}")
    print(f"    V['1']={V1:+.10f} | V['2']={V2:+.6f} | Qc(kJ/min)={Qc*meshr.FH_factor/1e3:.3f}")
    print(f"    Condenser residuals -> Mole bal: {mol_res:+.3e} | Energy bal: {eng_res:+.3e}")
    print(f"    Compare: L['1']={L1:+.10f} vs -Shell_Cost/1e6={-shell_scaled:+.10f}")
    if L1 < 0:
        print("    >>> NEGATIVE L['1'] REPRODUCED! Raw L.records (first 5 rows):")
        print(meshr.L.records.head(5).to_string(index=False))

def main():
    meshr = ReactiveDistillationModel(max_stages=22)
    try:
        for idx, (label, Ns, NFE, NFB, rxn) in enumerate(CASES):
            print("\n" + "=" * 82)
            print(f"{label} | Ns={Ns}, NFE={NFE}, NFB={NFB}, Rxn={rxn}")
            print("=" * 82)

            if hasattr(meshr, "reset_levels"):
                meshr.reset_levels()
            else:
                meshr._initialize_bounds_and_scales()

            meshr.update_config(Ns=Ns, NFE=NFE, NFB=NFB, reactive_trays=rxn)

            # 1. CONOPT warm-start
            meshr.model.solve(
                solver="CONOPT",
                options=gp.Options(time_limit=15, enable_scaling=True, relative_optimality_gap=1e-4, threads=1),
            )
            inspect_condenser(meshr, "CONOPT")

            # 2. BARON (print full solver log only on the first anomaly)
            meshr.model.solve(
                solver="BARON",
                options=gp.Options(time_limit=160, enable_scaling=True, relative_optimality_gap=1e-4, threads=1),
                solver_options=BARON_OPTS,
                output=sys.stdout if idx == 0 else None,
            )
            inspect_condenser(meshr, "BARON ")

            # 3. Also test BARON cold-start (without CONOPT warm-start) on first anomaly
            if idx == 0:
                if hasattr(meshr, "reset_levels"):
                    meshr.reset_levels()
                else:
                    meshr._initialize_bounds_and_scales()
                meshr._init_temp_and_hr()
                meshr.model.solve(
                    solver="BARON",
                    options=gp.Options(time_limit=160, enable_scaling=True, relative_optimality_gap=1e-4, threads=1),
                    solver_options=BARON_OPTS,
                )
                inspect_condenser(meshr, "BARON-COLD")
    finally:
        meshr.m.close()

if __name__ == "__main__":
    main()