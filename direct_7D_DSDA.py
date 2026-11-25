import os
import time
from datetime import datetime
import numpy as np
import pandas as pd
from scipy.optimize import direct, Bounds

from Direct.direct_class import DiscreteDirectWrapper, EarlyStopException
from functions.d_sda import DiscreteOptimizer


def save_cache_csv(cache_dict, csv_path, cols):
    if not cache_dict:
        return
    df = pd.Series(cache_dict).reset_index()
    df.columns = cols
    df.to_csv(csv_path, index=False, sep=";")


if __name__ == "__main__":
    os.makedirs("result", exist_ok=True)
    COLS_7D = ["Ns", "NFE", "NFB", "NR1", "NR2", "NR3", "NR4", "Profit"]

    # Instantiate once BEFORE timing so compilation time doesn't skew solver runtime
    optimizer_wrapper = DiscreteDirectWrapper(patience=20000)
    optimizer = DiscreteOptimizer(max_stages=22, meshr=optimizer_wrapper.meshr)

    bounds = Bounds(
        [7, 0, 0, 0, 0, 0, 0],
        [23, 1, 1, 1, 1, 1, 1],
    )

    try:
        # =====================================================================
        # Phase 1: DIRECT
        # =====================================================================
        print("Starting OOP DIRECT optimization (7D)...")
        t_direct_start = time.perf_counter()

        try:
            res_direct = direct(
                optimizer_wrapper.evaluate_7D,
                bounds=bounds,
                args=(),
                callback=optimizer_wrapper.callback,
                maxiter=200000,
                maxfun=2000000,
                len_tol=1 / 19,
            )

            mapped_vars, total_distance = optimizer_wrapper.map_discrete_variables(
                res_direct.x, max_Ns=optimizer_wrapper.max_Ns
            )
            final_x = [int(v) for v in mapped_vars]
            final_fun = float(res_direct.fun)
            status = res_direct.message

        except EarlyStopException as e:
            final_x = [int(v) for v in optimizer_wrapper.final_x]
            final_fun = float(optimizer_wrapper.final_fun)
            status = f"Stopped early: {e}"

        execution_time_Direct = time.perf_counter() - t_direct_start
        direct_cache_size = len(optimizer_wrapper.cache)

        # Copy cache so D-SDA does not mutate DIRECT's stats
        shared_cache = dict(optimizer_wrapper.cache)
        # save_cache_csv(shared_cache, "result/output_pandas_Direct_7D_short.csv", COLS_7D)

        # =====================================================================
        # Phase 2: D-SDA Warm-Started from DIRECT Best Solution
        # =====================================================================
        print("\n--- Direct into D-SDA ---")
        print(f"Initial D-SDA: {final_x} (Fobj = {final_fun:.6e}, ${final_fun * 1e6:,.2f}/yr)")

        res_dsda = optimizer.optimize(initial_y=final_x, cache=shared_cache)

        y_best = res_dsda["y_best"]
        fobj_best = res_dsda["fobj_best"]
        fobj_calls = res_dsda["evaluations"]
        time_spent = res_dsda["exec_time"]
        logs = res_dsda["line_search_log"]

        save_cache_csv(optimizer.cache_D_SDA, "result/output_pandas_DSDA_7D_short.csv", COLS_7D)

        # =====================================================================
        # Aggregate Summary & Logging
        # =====================================================================
        execution_time_Agg = execution_time_Direct + time_spent
        fobj_calls_Agg = optimizer_wrapper.counter + fobj_calls
        final_y_Agg = y_best
        final_fun_Agg = fobj_best

        print("\n--- Final Results (DIRECT + D-SDA 7D) ---")
        print(f"Total Execution time       : {execution_time_Agg:.4f} s (DIRECT: {execution_time_Direct:.2f} s | D-SDA: {time_spent:.2f} s)")
        print(f"DIRECT Status              : {status}")
        print(f"DIRECT unique evaluations  : {direct_cache_size} (solver calls: {optimizer_wrapper.counter})")
        print(f"D-SDA new solver calls     : {fobj_calls}")
        print(f"Total solver calls         : {fobj_calls_Agg}")
        print(f"Best Discrete X found      : {final_y_Agg}")
        print(f"Minimum Objective Value    : {final_fun_Agg:.6e} (${final_fun_Agg * 1e6:,.2f}/yr)")

        with open("result/Direct_D-SDA_7D_optimization_results.txt", "a") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Run date: {datetime.now()}\n")

            f.write(f"Execution time D-Direct + D-SDA: {execution_time_Agg:.6f} seconds\n")
            f.write(f"Objective functions calls: {fobj_calls_Agg}\n")
            f.write(f"Best Discrete X found: {final_y_Agg}\n")
            f.write(f"Minimum Objective Value: {final_fun_Agg:.6e}\n")

            f.write("\nDirect Results\n")
            f.write(f"Execution time: {execution_time_Direct:.6f} seconds\n")
            f.write(f"Status: {status}\n")
            f.write(f"Cache size (unique evaluations): {direct_cache_size}\n")
            f.write(f"Best Discrete X found: {final_x}\n")
            f.write(f"Minimum Objective Value: {final_fun:.6e}\n")
            f.write(f"Objective function evaluations: {optimizer_wrapper.counter}\n")

            f.write("\nD-SDA Results\n")
            f.write(f"Execution time: {time_spent:.6f} seconds\n")
            f.write(f"Objective functions calls: {fobj_calls}\n")
            f.write(f"Best Discrete X found: {y_best}\n")
            f.write(f"Minimum Objective Value: {fobj_best:.6e}\n")
    finally:
        # Clean up GAMSPy temporary working directory
        if hasattr(optimizer_wrapper, "meshr") and hasattr(optimizer_wrapper.meshr, "m"):
            optimizer_wrapper.meshr.m.close()