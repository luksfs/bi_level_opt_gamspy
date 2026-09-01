import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
# from gamspy_model.meshr_class_without_cat_res import ReactiveDistillationModel # without restriction
from gamspy_model.meshr_class import ReactiveDistillationModel  # new model
from functions.exhuaustive_comb import generate_scenarios_optimized
import time
from datetime import datetime
import os

def solve_scenario(config):

    meshr = ReactiveDistillationModel(max_stages=22)

    meshr.update_config(
        Ns=config["Ns"],
        NFE=config["NFE"],
        NFB=config["NFB"],
        reactive_trays=config["reactive"]
    )

    result = meshr.solve(solver="BARON")

    reactive = config["reactive"]

    return {
        "Ns": config["Ns"],
        "NFE": config["NFE"],
        "NFB": config["NFB"],
        "NR1": reactive[0] if len(reactive) > 0 else None,
        "NR2": reactive[1] if len(reactive) > 1 else None,
        "NR3": reactive[2] if len(reactive) > 2 else None,
        "NR4": reactive[3] if len(reactive) > 3 else None,
        "Status": result["Status"],
        "Profit": result["Profit"],
        "Dcol": meshr.col_diameter
    }

# from concurrent.futures import ProcessPoolExecutor
# import pandas as pd

if __name__ == "__main__":
    Nsmax = 22
    NRx = 4
    start_time = time.perf_counter()

    scenarios = generate_scenarios_optimized(Nsmax, NRx)

    with ProcessPoolExecutor(max_workers=10) as executor:

        results = list(executor.map(solve_scenario, scenarios))

    end_time = time.perf_counter()
    time = end_time - start_time
    df = pd.DataFrame(results)
    df.loc[df["Profit"] == 100000, "Profit"] = np.nan
    df = df.sort_values("Profit")

    ex_txt = f"exhaustive_{NRx+3}D"
    df.to_csv(os.path.join("result", ex_txt + ".csv"), index=False, sep=';')

    total_comb = len(scenarios)
    solved_space = df['Profit'].count()
    solved_space_perc = solved_space/total_comb*100
    best_sol = df.iloc[0,:]
    with open(os.path.join("result", ex_txt + ".txt"), "a") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Run date: {datetime.now()}\n")
        f.write(f"Execution time: {time:.6f} seconds\n")
        f.write(f"Nsmax: {Nsmax}\n")
        f.write(f"Total combinatory space: {total_comb}\n")
        f.write(f"Solved candidates: {solved_space}\n")
        f.write(f"Solved candidates %: {solved_space_perc}\n")
        f.write(f"Minimum Objective Value and design variables: \n")
        line = "; ".join(f"{col}={best_sol[col]}" for col in df.columns)
        f.write(line + "\n")
    