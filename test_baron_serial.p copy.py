import sys
import gamspy as gp
from gamspy_model.meshr_class import ReactiveDistillationModel

CASES = [
    {"Ns": 8,  "NFE": 3, "NFB": 6,  "reactive": [3, 4, 6]},
    {"Ns": 10, "NFE": 3, "NFB": 8,  "reactive": [4, 5, 6]},
    {"Ns": 14, "NFE": 5, "NFB": 11, "reactive": [3, 7, 11]},
    {"Ns": 18, "NFE": 6, "NFB": 15, "reactive": [6, 11, 15]},
]

BARON_OPTS = {
    "AllowExternal": 0, "AllowMinos": 0, "AllowSnopt": 0,
    "NumLoc": 1, "Threads": 1, "MaxTime": 160,
}

meshr = ReactiveDistillationModel(max_stages=22)
try:
    for idx, cfg in enumerate(CASES):
        if hasattr(meshr, "reset_levels"):
            meshr.reset_levels()
        else:
            meshr._initialize_bounds_and_scales()

        meshr.update_config(Ns=cfg["Ns"], NFE=cfg["NFE"], NFB=cfg["NFB"], reactive_trays=cfg["reactive"])
        meshr.solve(solver="CONOPT", time_limit=15)

        meshr.model.solve(
            solver="BARON",
            options=gp.Options(time_limit=160, enable_scaling=True, relative_optimality_gap=1e-4, threads=1),
            solver_options=BARON_OPTS,
            output=sys.stdout if idx == 3 else None,
        )
        L1 = float(meshr.L.records.set_index("j").loc["1", "level"])
        V2 = float(meshr.V.records.set_index("j").loc["2", "level"])
        D  = float(meshr.D.toValue())
        print(f"Case {idx+1} (Ns={cfg['Ns']}): L1={L1:+.6f} | V2-D={V2-D:+.6f} | RR_L1={L1/D:+.4f} | RR_V2={(V2-D)/D:+.4f}")
finally:
    meshr.m.close()