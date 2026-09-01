from Direct.direct_class import DiscreteDirectWrapper, EarlyStopException
from scipy.optimize import direct, Bounds
import numpy as np
import time
from datetime import datetime
from functions.d_sda import DiscreteOptimizer

start_time = time.perf_counter()
# Instantiate the class
optimizer_wrapper = DiscreteDirectWrapper( 
    patience=20000
)

# Set bounds
bounds = Bounds([4.9 , 0, 0, 0],
                [22.1, 1, 1, 1])

# vol_tol_spec = 1/17*1/18

print("Starting OOP DIRECT optimization...")

try:
    # Notice how we pass optimizer_wrapper.evaluate and optimizer_wrapper.callback
    result = direct(
        optimizer_wrapper.evaluate_4D,
        bounds=bounds,
        args=(),
        callback=optimizer_wrapper.callback,
        maxiter=20000,
        maxfun=20000,
        len_tol=1/20.1,
        # vol_tol=vol_tol_spec
    )

    Ns_c, NFE_c, NFB_c, NR1_c = result.x
    # If it finishes naturally without triggering the early stop:
    Ns = int(np.round(Ns_c))
    
    NFE = int( np.round( 2 + NFE_c * (Ns - 4)) )
    NFB = int( np.round( NFE + NFB_c * (Ns - 2 - NFE) ) )
    NR1 = int( np.round( 2 + NR1_c * (Ns - 4) ) )

    final_x = [Ns,NFE, NFB, NR1]
    # final_x = np.round(result.x).astype(int)
    final_fun = result.fun
    status = result.message
    
except EarlyStopException as e:
    # If we catch our controlled crash, pull the results from the class instance
    final_x = optimizer_wrapper.final_x
    final_fun = optimizer_wrapper.final_fun
    status = f"Stopped early: {e}"

# End Direcct - Calc exc time
end_time = time.perf_counter()
execution_time_Direct = end_time - start_time

# You can persist this dictionary if you run multiple times or save it to a pickle file
shared_cache = optimizer_wrapper.cache

# Instantiate the optimizer once
optimizer = DiscreteOptimizer(max_stages=22)

# User provides initial variables directly with arbitrary lengths
# Example 1: 4 Variables
# initial_y = [14, 7, 10, 7] 

# Example 2: 7 Variables [Ns, NFE, NFB, NR1, NR2, NR3, NR4]
# initial_y = [7, 4, 4, 4, 5]
print("\n--- Direct into  D-SDA ---")
print("\n Initial D-SDA {final_x}")

initial_y = final_x

# Run the optimization
result = optimizer.optimize(initial_y=initial_y, cache=shared_cache)

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
fobj_calls_Agg = optimizer_wrapper.counter + fobj_calls
final_y_Agg = y_best
final_fun_Agg = fobj_best

print(f"Execution time: {execution_time_Agg:.6f} seconds")
# print(f"Status: {status}")
# print(f"Cache size (unique evaluations): {len(optimizer_wrapper.cache)}")
print(f"Best Discrete X found: {final_y_Agg}")
print(f"Minimum Objective Value: {final_fun_Agg}")
print(f"Objective function evaluations: {fobj_calls_Agg}")

with open("result/Direct_D-SDA_4D_optimization_results.txt", "a") as f:
    f.write(f"\n{'='*50}\n")
    f.write(f"Run date: {datetime.now()}\n")

    # Agregate Results D-Direct + D-SDA
    f.write(f"Execution time D-Direct + D-SDA: {execution_time_Agg:.6f} seconds\n")
    f.write(f"Objective functions calls: {fobj_calls_Agg}\n")
    f.write(f"Best Discrete X found: {final_y_Agg}\n")
    f.write(f"Minimum Objective Value: {final_fun_Agg}\n")

    # Direct
    f.write(f"\n")
    f.write(f"Direct Results\n")
    f.write(f"Execution time: {execution_time_Direct:.6f} seconds\n")
    f.write(f"Status: {status}\n")
    f.write(f"Cache size (unique evaluations): {len(optimizer_wrapper.cache)}\n")
    f.write(f"Best Discrete X found: {final_x}\n")
    f.write(f"Minimum Objective Value: {final_fun}\n")
    f.write(f"Objective function evaluations: {optimizer_wrapper.counter}\n")

    # D-SDA
    f.write(f"\n")
    f.write(f"D-SDA Results\n")
    f.write(f"Execution time: {time_spent:.6f} seconds\n")
    f.write(f"Objective functions calls: {fobj_calls}\n")
    f.write(f"Best Discrete X found: {y_best}\n")
    f.write(f"Minimum Objective Value: {fobj_best}\n")