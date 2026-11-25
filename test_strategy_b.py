import time
from gamspy_model.meshr_class import ReactiveDistillationModel

CASES = [
    {"Ns": 8,  "NFE": 3, "NFB": 6,  "reactive": [3, 4, 6]},
    {"Ns": 10, "NFE": 3, "NFB": 8,  "reactive": [4, 5, 6]},
    {"Ns": 14, "NFE": 5, "NFB": 11, "reactive": [3, 7, 11]},
    {"Ns": 18, "NFE": 6, "NFB": 15, "reactive": [6, 11, 15]},
]

meshr = ReactiveDistillationModel(max_stages=22)
try:
    print(f"{'Ns':>3} | {'Status':24s} | {'Time':>5} | {'TAC($/yr)':>10} | {'Dcol(m)':>7} | {'ht(m)':>6} | {'L/D':>5} | {'Flood%':>11} | {'RR':>5}")
    print("-" * 98)
    for cfg in CASES:
        if hasattr(meshr, "reset_levels"):
            meshr.reset_levels()
        else:
            meshr._initialize_bounds_and_scales()

        meshr.update_config(Ns=cfg["Ns"], NFE=cfg["NFE"], NFB=cfg["NFB"], reactive_trays=cfg["reactive"])
        meshr.solve(solver="CONOPT", time_limit=15)
        t0 = time.perf_counter()
        res = meshr.solve(solver="BARON", time_limit=160)
        dt = time.perf_counter() - t0

        Ns = cfg["Ns"]
        j_int = [str(s) for s in range(2, Ns)]
        uf  = meshr.uf.records.set_index("j").loc[j_int, "level"].values
        ufl = meshr.ufl.records.set_index("j").loc[j_int, "level"].values
        fl  = 100.0 * uf / ufl
        Dcol = meshr.Dcol.toValue()
        ht   = meshr.ht.toValue()
        LD   = (1.0 + meshr.SF) * ht * (Ns - 2) / Dcol
        RR   = meshr.L.records.set_index("j").loc["1", "level"] / meshr.D.toValue()
        tac  = res["Profit"] * 1e6

        print(f"{Ns:3d} | {str(res['Status']):24s} | {dt:4.1f}s | {tac:10.2f} | {Dcol:7.4f} | {ht:6.4f} | {LD:5.2f} | {fl.min():4.1f}-{fl.max():4.1f}% | {RR:5.2f}")
finally:
    meshr.m.close()