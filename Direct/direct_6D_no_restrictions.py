from direct_class import DiscreteDirectWrapper, EarlyStopException
from scipy.optimize import direct, Bounds
import numpy as np
# import pandas as pd

# Instantiate the class
optimizer_wrapper = DiscreteDirectWrapper( 
    patience=20000
)

# Set bounds
bounds = Bounds([4.9 , 0, 0, 0, 0, 0],
                [22.1, 1, 1, 1, 1, 1])

print("Starting OOP DIRECT optimization...")

try:
    # Notice how we pass optimizer_wrapper.evaluate and optimizer_wrapper.callback
    result = direct(
        optimizer_wrapper.evaluate_6D,
        bounds=bounds,
        args=(),
        callback=optimizer_wrapper.callback,
        maxiter=20000,
        maxfun=20000,
        len_tol=1/22.1
    )

    Ns_c, NFE_c, NFB_c, NR1_c, NR2_c, NR3_c = result.x
    # If it finishes naturally without triggering the early stop:
    Ns = int(np.round(Ns_c))
    NFE = int( np.round( 1 + NFE_c * (Ns - 3)) )
    NFB = int( np.round( NFE + NFB_c * (Ns - 2 - NFE) ) )
    NR1 = int( np.round( 1 + NR1_c * (Ns - 5) ) )
    NR2 = int( np.round( NR1 + 1 + NR2_c * (Ns - 4 - NR1) ) )
    NR3 = int( np.round( NR2 + 1 + NR3_c * (Ns - 3 - NR2) ) )
    
    final_x = [Ns,NFE, NFB, NR1, NR2, NR3]
    # final_x = np.round(result.x).astype(int)
    final_fun = result.fun
    status = result.message
    
except EarlyStopException as e:
    # If we catch our controlled crash, pull the results from the class instance
    final_x = optimizer_wrapper.final_x
    final_fun = optimizer_wrapper.final_fun
    status = f"Stopped early: {e}"

print("\n--- Final Results ---")
print(f"Status: {status}")
print(f"Cache size (unique evaluations): {len(optimizer_wrapper.cache)}")
print(f"Best Discrete X found: {final_x}")
print(f"Minimum Objective Value: {final_fun}")
print(f"Objective function evaluations: {optimizer_wrapper.counter}")