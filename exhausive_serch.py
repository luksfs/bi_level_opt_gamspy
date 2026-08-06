import random
import statistics
from functions.comb_manager import CombinationManager
# from gamspy_model.meshr_class_without_cat_res import ReactiveDistillationModel
import numpy as np
import time
from datetime import datetime

import pandas as pd
from itertools import product
from concurrent.futures import ProcessPoolExecutor
from gamspy_model.meshr_class_without_cat_res import ReactiveDistillationModel

def solve_scenario(config):
    """
    Each process creates its own model, updates the configuration,
    solves it, and returns the results.
    """

    # Create model inside the process
    meshr = ReactiveDistillationModel(max_stages=22)

    meshr.update_config(
        Ns=config["Ns"],
        NFE=config["NFE"],
        NFB=config["NFB"],
        reactive_trays=config["reactive"]
    )

    result = meshr.solve(solver="BARON")

    return {
        "Ns": config["Ns"],
        "NFE": config["NFE"],
        "NFB": config["NFB"],
        "NR1": config["reactive"][0] if len(config["reactive"]) > 0 else None,
        "NR2": config["reactive"][1] if len(config["reactive"]) > 1 else None,
        "NR3": config["reactive"][2] if len(config["reactive"]) > 2 else None,
        "NR4": config["reactive"][3] if len(config["reactive"]) > 3 else None,
        "Status": result["Status"],
        "Profit": result["Profit"]
    }


if __name__ == "__main__":

    Ns = 7
    NFB = 3

    scenarios = []

    for NFE, NR1 in product(range(2, Ns), range(2, Ns)):
        scenarios.append({
            "Ns": Ns,
            "NFE": NFE,
            "NFB": NFB,
            "reactive": [NR1]
        })
    # scenarios = [
    #     {"Ns": 10, "NFE": 5, "NFB": 7, "reactive": [3, 5, 7]},
    #     {"Ns": 7, "NFE": 3, "NFB": 3, "reactive": [3]},
    #     {"Ns": 10, "NFE": 5, "NFB": 7, "reactive": [3, 5, 6, 7]},
    # ]

    with ProcessPoolExecutor(max_workers=3) as executor:

        results = list(executor.map(solve_scenario, scenarios))
        
    df = pd.DataFrame(results)
    df.loc[df["Status"] == "fail", "Profit"] = np.nan
    print(df)

    df.to_csv("results.csv", index=False,sep=';')

    import matplotlib.pyplot as plt
    import seaborn as sns

    
    grid = df.pivot(
        index="NR1",
        columns="NFE",
        values="Profit"
    )
    
    fig, ax = plt.subplots(figsize=(8,6))
    im = ax.imshow(
        grid,
        origin="lower",
        cmap="viridis_r"
    )

    ax.set_xticks(range(len(grid.columns)))
    ax.set_xticklabels(grid.columns)

    ax.set_yticks(range(len(grid.index)))
    ax.set_yticklabels(grid.index)

    sns.heatmap(
        grid*100,
        annot=True,
        cmap="viridis",
        fmt='.3f',
        linewidths=1,
        linecolor='white',
        ax=ax,
        vmax=2.6
    )
    plt.colorbar(im, label="Objective")
    plt.xlabel("NFE")
    plt.ylabel("NR1")

    plt.show()
