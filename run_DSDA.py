import os
import csv
import time
from functions.d_sda import DiscreteOptimizer


def run_dsda(initial_y, optimizer, max_stages=22):
    dim = len(initial_y)
    if dim < 4:
        raise ValueError(f"Expected at least 4 variables [Ns, NFE, NFB, NR1, ...], got {initial_y}")

    os.makedirs("result", exist_ok=True)
    csv_path = os.path.join("result", f"D-SDA_{dim}D.csv")

    print(f"\n--- Running D-SDA ({dim}D) | initial_y = {initial_y} ---")
    start_time = time.perf_counter()
    result = optimizer.optimize(initial_y=initial_y, cache={})
    exec_time = time.perf_counter() - start_time

    y_best = result["y_best"]
    fobj_best = result["fobj_best"]
    fobj_calls = result["evaluations"]

    print(f"\n--- Final Results ({dim}D) ---")
    print(f"Execution time             : {exec_time:.4f} s")
    print(f"Best Discrete X found      : {y_best}")
    print(f"Minimum Objective Value    : {fobj_best:.6e} (${fobj_best * 1e6:,.2f}/yr)")
    print(f"Objective function calls   : {fobj_calls}")

    write_header = not os.path.isfile(csv_path) or os.path.getsize(csv_path) == 0
    with open(csv_path, mode="a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        if write_header:
            writer.writerow(["initial_y", "y_best", "fobj_best", "exec_time_s", "evaluations"])
        writer.writerow([initial_y, y_best, fobj_best, exec_time, fobj_calls])

    return result


if __name__ == "__main__":
    # Pick one configuration (or uncomment multiple to run 4D-7D sequentially without recompiling)
    INITIAL_CONFIGS = [
        [14, 8, 8, 8],          # 4D (1 reactive tray)
        # [14, 8, 8, 7, 8],     # 5D (2 reactive trays)
        # [14, 8, 8, 6, 7, 8],  # 6D (3 reactive trays)
        # [14, 8, 8, 5, 6, 7, 8], # 7D (4 reactive trays)
    ]

    optimizer = DiscreteOptimizer(max_stages=22)
    try:
        for init_y in INITIAL_CONFIGS:
            run_dsda(init_y, optimizer=optimizer)
    finally:
        # Clean up GAMSPy temp directory on exit
        if hasattr(optimizer, "meshr") and hasattr(optimizer.meshr, "m"):
            optimizer.meshr.m.close()