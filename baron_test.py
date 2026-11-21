import sys
import gamspy as gp
from gamspy_model.meshr_class import ReactiveDistillationModel

meshr = ReactiveDistillationModel(max_stages=22)
meshr.update_config(Ns=13, NFE=9, NFB=9, reactive_trays=[2, 4, 6])
meshr.model.solve(
    solver="BARON",
    options=gp.Options(time_limit=160, enable_scaling=True, relative_optimality_gap=1e-4, threads=1),
    solver_options={
        "AllowExternal": 0,
        "AllowMinos": 0,
        "AllowSnopt": 0,
        "Threads": 1,
        "MaxTime": 160,
    },
    output=sys.stdout,
)
meshr.m.close()