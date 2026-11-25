import os
import time
from datetime import datetime
import pandas as pd
from scipy.optimize import direct, Bounds

from Direct.direct_class import DiscreteDirectWrapper, EarlyStopException
from functions.d_sda import DiscreteOptimizer


# Minimum valid Ns for each dimension (needs at least NRx internal stages + condenser + reboiler)
NS_MIN_BY_DIM = {
    4: 4,  # 1 reactive tray
    5: 5,  # 2 reactive trays
    6: 6,  # 3 reactive trays
    7: 7,  # 4 reactive trays
}


def compute_len_tol(ns_min, ns_max, target_pts_per_side):
    """
    Returns a SciPy DIRECT len_tol strictly above the coarsest (1/3)^k side length
    that satisfies (max_discrete_span * (1/3)^k) <= target_pts_per_side.
    - target_pts_per_side = 2 -> stops at ~1-2 discrete pts/side (DIRECT + D-SDA)
    - target_pts_per_side = 1 -> stops at <= 1 discrete pt/side  (DIRECT-only)
    """
    max_span = max(ns_max - ns_min + 1, ns_max - 2)
    k = 1
    while max_span * ((1.0 / 3.0) ** k) > target_pts_per_side:
        k += 1
    L_k = (1.0 / 3.0) ** k
    # Small +1e-4 margin prevents float rounding from pushing DIRECT into k+1
    return L_k + 1e-4, k, L_k


def save_cache_csv(cache_dict, csv_path, cols):
    if not cache_dict:
        return
    df = pd.Series(cache_dict).reset_index()
    df.columns = cols
    df.to_csv(csv_path, index=False, sep=";")


def run_experiment(
    dim,
    ns_max=12,
    run_dsda=True,
    len_tol=None,
    patience=20000,
    maxiter=200000,
    maxfun=200000,
    max_stages=22,
):
    if dim not in NS_MIN_BY_DIM:
        raise ValueError(f"dim must be one of {list(NS_MIN_BY_DIM.keys())}, got {dim}")

    os.makedirs("result", exist_ok=True)
    n_rxn = dim - 3
    ns_min = NS_MIN_BY_DIM[dim]
    cols = ["Ns", "NFE", "NFB"] + [f"NR{k}" for k in range(1, n_rxn + 1)] + ["Profit"]
    mode_tag = "Direct_DSDA" if run_dsda else "Direct_only"

    # Choose len_tol automatically unless explicitly overridden
    if len_tol is None:
        target_pts = 2.0 if run_dsda else 1.0
        len_tol, k_splits, L_k = compute_len_tol(ns_min, ns_max, target_pts)
        print(
            f"[{dim}D | {mode_tag} | Ns in [{ns_min}, {ns_max}]] "
            f"Auto len_tol = {len_tol:.5f} (stops at k={k_splits}, L=1/{3**k_splits}={L_k:.4f})"
        )
    else:
        print(f"[{dim}D | {mode_tag} | Ns in [{ns_min}, {ns_max}]] Manual len_tol = {len_tol:.5f}")

    # Bounds: [ns_min, ns_max + 1] on Ns so floor(Ns_c) covers {ns_min, ..., ns_max}
    lb = [ns_min] + [0] * (dim - 1)
    ub = [ns_max + 1] + [1] * (dim - 1)
    bounds = Bounds(lb, ub)

    # Instantiate once BEFORE timing so compilation time doesn't skew solver runtime
    optimizer_wrapper = DiscreteDirectWrapper(patience=patience)
    optimizer_wrapper.max_Ns = ns_max  # Keep wrapper decoding aligned with Bounds
    eval_fn = getattr(optimizer_wrapper, f"evaluate_{dim}D")

    optimizer = (
        DiscreteOptimizer(max_stages=max_stages, meshr=optimizer_wrapper.meshr)
        if run_dsda
        else None
    )

    try:
        # =====================================================================
        # Phase 1: DIRECT
        # =====================================================================
        print(f"Starting OOP DIRECT optimization ({dim}D)...")
        t_direct_start = time.perf_counter()

        try:
            res_direct = direct(
                eval_fn,
                bounds=bounds,
                args=(),
                callback=optimizer_wrapper.callback,
                maxiter=maxiter,
                maxfun=maxfun,
                len_tol=len_tol,
            )

            mapped_vars, _ = optimizer_wrapper.map_discrete_variables(
                res_direct.x, max_Ns=optimizer_wrapper.max_Ns
            )
            final_x = [int(v) for v in mapped_vars]
            final_fun = float(res_direct.fun)
            status = res_direct.message

        except EarlyStopException as e:
            final_x = [int(v) for v in optimizer_wrapper.final_x]
            final_fun = float(optimizer_wrapper.final_fun)
            status = f"Stopped early: {e}"

        execution_time_direct = time.perf_counter() - t_direct_start
        direct_cache_size = len(optimizer_wrapper.cache)
        direct_calls = optimizer_wrapper.counter

        # Copy cache BEFORE D-SDA so DIRECT's cache stats remain untouched
        direct_cache_copy = dict(optimizer_wrapper.cache)
        save_cache_csv(
            direct_cache_copy,
            os.path.join("result", f"output_pandas_Direct_{dim}D_NS{ns_max}_{mode_tag}.csv"),
            cols,
        )

        # =====================================================================
        # Phase 2: Optional D-SDA Refinement
        # =====================================================================
        if run_dsda:
            print("\n--- Direct into D-SDA ---")
            print(f"Initial D-SDA: {final_x} (Fobj = {final_fun:.6e}, ${final_fun * 1e6:,.2f}/yr)")

            res_dsda = optimizer.optimize(initial_y=final_x, cache=direct_cache_copy)
            y_best = res_dsda["y_best"]
            fobj_best = res_dsda["fobj_best"]
            dsda_calls = res_dsda["evaluations"]
            dsda_time = res_dsda["exec_time"]

            save_cache_csv(
                optimizer.cache_D_SDA,
                os.path.join("result", f"output_pandas_DSDA_{dim}D_NS{ns_max}.csv"),
                cols,
            )
        else:
            y_best = final_x
            fobj_best = final_fun
            dsda_calls = 0
            dsda_time = 0.0

        # =====================================================================
        # Summary & Logging
        # =====================================================================
        execution_time_agg = execution_time_direct + dsda_time
        fobj_calls_agg = direct_calls + dsda_calls

        print(f"\n--- Final Results ({dim}D | {mode_tag} | Ns_max={ns_max}) ---")
        print(f"Total Execution time       : {execution_time_agg:.4f} s (DIRECT: {execution_time_direct:.2f} s | D-SDA: {dsda_time:.2f} s)")
        print(f"DIRECT Status              : {status}")
        print(f"DIRECT unique evaluations  : {direct_cache_size} (solver calls: {direct_calls})")
        if run_dsda:
            print(f"D-SDA new solver calls     : {dsda_calls}")
        print(f"Total solver calls         : {fobj_calls_agg}")
        print(f"Best Discrete X found      : {y_best}")
        print(f"Minimum Objective Value    : {fobj_best:.6e} (${fobj_best * 1e6:,.2f}/yr)")

        log_path = os.path.join("result", f"{mode_tag}_{dim}D_NS{ns_max}_optimization_results.txt")
        with open(log_path, "a") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Run date: {datetime.now()}\n")
            f.write(f"Mode: {mode_tag} | Dim: {dim}D | Ns_range: [{ns_min}, {ns_max}] | len_tol: {len_tol}\n")
            f.write(f"Execution time Total: {execution_time_agg:.6f} seconds\n")
            f.write(f"Objective function calls: {fobj_calls_agg}\n")
            f.write(f"Best Discrete X found: {y_best}\n")
            f.write(f"Minimum Objective Value: {fobj_best:.6e}\n")

            f.write("\nDirect Results\n")
            f.write(f"Execution time: {execution_time_direct:.6f} seconds\n")
            f.write(f"Status: {status}\n")
            f.write(f"Cache size (unique evaluations): {direct_cache_size}\n")
            f.write(f"Best Discrete X found: {final_x}\n")
            f.write(f"Minimum Objective Value: {final_fun:.6e}\n")
            f.write(f"Objective function evaluations: {direct_calls}\n")

            if run_dsda:
                f.write("\nD-SDA Results\n")
                f.write(f"Execution time: {dsda_time:.6f} seconds\n")
                f.write(f"Objective function calls: {dsda_calls}\n")
                f.write(f"Best Discrete X found: {y_best}\n")
                f.write(f"Minimum Objective Value: {fobj_best:.6e}\n")

        return {
            "y_best": y_best,
            "fobj_best": fobj_best,
            "total_calls": fobj_calls_agg,
            "total_time_s": execution_time_agg,
        }
    finally:
        if hasattr(optimizer_wrapper, "meshr") and hasattr(optimizer_wrapper.meshr, "m"):
            optimizer_wrapper.meshr.m.close()


if __name__ == "__main__":
    # Example 1: DIRECT + D-SDA (stops DIRECT at ~2 pts/side, then refines with D-SDA)
    for d in [4, 5, 6, 7]:
        run_experiment(dim=d, ns_max=22, run_dsda=True)

    # Example 2: DIRECT-only (stops DIRECT at <= 1 pt/side, no D-SDA)
    # for d in [4, 5, 6]:
    #     run_experiment(dim=d, ns_max=14, run_dsda=False)