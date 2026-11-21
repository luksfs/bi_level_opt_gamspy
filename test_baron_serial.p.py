import sys
import time
import gamspy as gp
from gamspy_model.meshr_class import ReactiveDistillationModel

CASES = [
    {
        "label": "Infeasible check (previously 57.6 s)",
        "Ns": 13, "NFE": 9, "NFB": 9, "reactive": [2, 4, 6],
    },
    {
        "label": "Feasible benchmark (Bernal et al. 2018)",
        "Ns": 10, "NFE": 3, "NFB": 8, "reactive": [4, 5, 6],
    },
]

BARON_OPTS = {
    "AllowExternal": 0,
    "AllowMinos": 0,
    "AllowSnopt": 0,
    "NumLoc": 1,
    "Threads": 1,
    "MaxTime": 160,
}

def main():
    meshr = ReactiveDistillationModel(max_stages=22)
    summary = []

    try:
        for case in CASES:
            print("\n" + "#" * 78)
            print(f"CASE: {case['label']}")
            print(f"  Ns={case['Ns']}, NFE={case['NFE']}, NFB={case['NFB']}, Rxn={case['reactive']}")
            print("#" * 78)

            # Reset starting levels cleanly between cases
            if hasattr(meshr, "reset_levels"):
                meshr.reset_levels()
            else:
                meshr._initialize_bounds_and_scales()

            meshr.update_config(
                Ns=case["Ns"],
                NFE=case["NFE"],
                NFB=case["NFB"],
                reactive_trays=case["reactive"],
            )

            # Step 1: Fast CONOPT warm-start
            t0 = time.perf_counter()
            meshr.model.solve(
                solver="CONOPT",
                options=gp.Options(
                    time_limit=15,
                    enable_scaling=True,
                    relative_optimality_gap=1e-4,
                    threads=1,
                ),
            )
            t_conopt = time.perf_counter() - t0
            conopt_status = meshr.model.status
            conopt_ok = getattr(conopt_status, "value", -1) in (1, 2)
            conopt_obj = meshr.obj.toValue() if conopt_ok else float("nan")
            print(f"\n[CONOPT warm-start] Status={conopt_status} | Obj={conopt_obj:.6e} | Time={t_conopt:.2f} s")

            # If CONOPT failed, reset levels so BARON does not start from a diverged point
            if not conopt_ok:
                if hasattr(meshr, "reset_levels"):
                    meshr.reset_levels()
                else:
                    meshr._initialize_bounds_and_scales()
                meshr._init_temp_and_hr()

            # Step 2: BARON global proof (with full log printed to terminal)
            print("\n[BARON global solve] Starting...\n")
            t1 = time.perf_counter()
            meshr.model.solve(
                solver="BARON",
                options=gp.Options(
                    time_limit=160,
                    enable_scaling=True,
                    relative_optimality_gap=1e-4,
                    threads=1,
                ),
                solver_options=BARON_OPTS,
                output=sys.stdout,
            )
            t_baron = time.perf_counter() - t1
            baron_status = meshr.model.status
            baron_ok = getattr(baron_status, "value", -1) in (1, 2)
            baron_obj = meshr.obj.toValue() if baron_ok else float("nan")

            summary.append({
                "label": case["label"],
                "conopt_status": str(conopt_status),
                "conopt_obj": conopt_obj,
                "conopt_s": t_conopt,
                "baron_status": str(baron_status),
                "baron_obj": baron_obj,
                "baron_s": t_baron,
            })
    finally:
        meshr.m.close()

    print("\n" + "=" * 78)
    print("SERIAL TEST SUMMARY")
    print("=" * 78)
    for row in summary:
        print(
            f"{row['label']}\n"
            f"  CONOPT: {row['conopt_status']:28s} | Obj={row['conopt_obj']:.6e} | {row['conopt_s']:6.2f} s\n"
            f"  BARON : {row['baron_status']:28s} | Obj={row['baron_obj']:.6e} | {row['baron_s']:6.2f} s"
        )

if __name__ == "__main__":
    main()