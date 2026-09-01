from Direct.direct_class import DiscreteDirectWrapper, EarlyStopException
from scipy.optimize import direct, Bounds
import numpy as np
import time
from datetime import datetime
from functions.d_sda import DiscreteOptimizer
import csv
import random

for i in range(5):
    start_time = time.perf_counter()

    # Instantiate the optimizer once
    optimizer = DiscreteOptimizer(max_stages=22)

    # User provides initial variables directly with arbitrary lengths
    # Example 1: 4 Variables
    # initial_y = [14, 7, 10, 7] 

    # Example 2: 7 Variables [Ns, NFE, NFB, NR1, NR2, NR3, NR4]
    # initial_y = [7, 4, 4, 4, 5]
    print("\n--- Direct into  D-SDA ---")
    # print("\n Initial D-SDA {final_x}")

    Ns  = random.randint(6, 22)
    NFE = random.randint(2, Ns-1)
    NFB = random.randint(NFE, Ns-1)
    NR1 = random.randint(2, Ns-4)
    NR2 = random.randint(NR1+1, Ns-3)
    NR3 = random.randint(NR2+1, Ns-2)

    initial_y = [Ns, NFE, NFB, NR1, NR2, NR3]
    # initial_y = [9, 4, 6, 3, 6]
    # Run the optimization
    result = optimizer.optimize(initial_y=initial_y, cache={})

    # Extract results
    y_best = result['y_best']
    fobj_best = result['fobj_best']
    fobj_calls = result['evaluations']
    time_spent = result['exec_time']
    logs = result['line_search_log']


    print("\n--- Final Results ---")
    # End Direct + D_SDA
    end_time = time.perf_counter()
    execution_time_Agg = end_time - start_time
    fobj_calls_Agg = fobj_calls
    final_y_Agg = y_best
    final_fun_Agg = fobj_best

    print(f"Execution time: {execution_time_Agg:.6f} seconds")
    # print(f"Status: {status}")
    # print(f"Cache size (unique evaluations): {len(optimizer_wrapper.cache)}")
    print(f"Best Discrete X found: {final_y_Agg}")
    print(f"Minimum Objective Value: {final_fun_Agg}")
    print(f"Objective function evaluations: {fobj_calls_Agg}")

    with open('result/D-SDA_6D.csv', mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        new_row = [initial_y, y_best, fobj_best, execution_time_Agg, fobj_calls]
        writer.writerow(new_row)

    with open("result/D-SDA_6D_optimization_results.txt", "a") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Run date: {datetime.now()}\n")
        # D-SDA
        f.write(f"\n")
        f.write(f"D-SDA Results\n")
        f.write(f"Execution time: {time_spent:.6f} seconds\n")
        f.write(f"Objective functions calls: {fobj_calls}\n")
        f.write(f"Best Discrete X found: {y_best}\n")
        f.write(f"Minimum Objective Value: {fobj_best}\n")