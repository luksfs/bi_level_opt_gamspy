from Direct.direct_class import DiscreteDirectWrapper, EarlyStopException
from scipy.optimize import direct, Bounds
import numpy as np
import time
from datetime import datetime

start_time = time.perf_counter()
# Instantiate the class
optimizer_wrapper = DiscreteDirectWrapper( 
    patience=20000
)

# Set bounds
bounds = Bounds([4.9 , 0, 0, 0, 0],
                [22.1, 1, 1, 1, 1])

print("Starting OOP DIRECT optimization...")

try:
    # Notice how we pass optimizer_wrapper.evaluate and optimizer_wrapper.callback
    result = direct(
        optimizer_wrapper.evaluate_5D,
        bounds=bounds,
        args=(),
        callback=optimizer_wrapper.callback,
        maxiter=20000,
        maxfun=20000,
        len_tol=1/22.1
    )

    Ns_c, NFE_c, NFB_c, NR1_c, NR2_c = result.x
    # If it finishes naturally without triggering the early stop:
    Ns = int(np.round(Ns_c))
    
    NFE = int( np.round( 2 + NFE_c * (Ns - 4)) )
    NFB = int( np.round( NFE + NFB_c * (Ns - 2 - NFE) ) )
    NR1 = int( np.round( 2 + NR1_c * (Ns - 5) ) )
    NR2 = int( np.round( NR1 + 1 + NR2_c * (Ns - 3 - NR1) ) )

    final_x = [Ns,NFE, NFB, NR1, NR2]
    # final_x = np.round(result.x).astype(int)
    final_fun = result.fun
    status = result.message
    
except EarlyStopException as e:
    # If we catch our controlled crash, pull the results from the class instance
    final_x = optimizer_wrapper.final_x
    final_fun = optimizer_wrapper.final_fun
    status = f"Stopped early: {e}"

print("\n--- Final Results ---")
end_time = time.perf_counter()

# 3. Calculate and print the difference
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.6f} seconds")
print(f"Status: {status}")
print(f"Cache size (unique evaluations): {len(optimizer_wrapper.cache)}")
print(f"Best Discrete X found: {final_x}")
print(f"Minimum Objective Value: {final_fun}")
print(f"Objective function evaluations: {optimizer_wrapper.counter}")

# Save results
with open("result/Direct_5D_optimization_results.txt", "a") as f:
    f.write(f"\n{'='*50}\n")
    f.write(f"Run date: {datetime.now()}\n")
    f.write(f"Execution time: {execution_time:.6f} seconds\n")
    f.write(f"Status: {status}\n")
    f.write(f"Cache size (unique evaluations): {len(optimizer_wrapper.cache)}\n")
    f.write(f"Best Discrete X found: {final_x}\n")
    f.write(f"Minimum Objective Value: {final_fun}\n")
    f.write(f"Objective function evaluations: {optimizer_wrapper.counter}\n")