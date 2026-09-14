import time
from datetime import datetime
from functions.comb_manager import CombinationManager
from functions.invalid_check import check_bounds
import os
import sys

# # 1. Get the path of the current directory (the 'functions' folder)
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # 2. Get the path of the parent directory (the root folder)
# parent_dir = os.path.dirname(current_dir)

# # 3. Add the parent directory to sys.path so Python can find 'gamspy_model'
# if parent_dir not in sys.path:
#     sys.path.insert(0, parent_dir)

# 4. Now you can safely import your class
from gamspy_model.meshr_class import ReactiveDistillationModel

class DiscreteOptimizer:
    def __init__(self, max_stages=22):
        """Initialize the model and the evaluation tracker."""
        self.meshr = ReactiveDistillationModel(max_stages=max_stages)
        self.eval_calls = 0
        self.cache = {}
        self.line_search_log = []
        self.cache_D_SDA = {}
        
    def evaluate(self, y):
        """
        Evaluates the objective function. 
        Checks the cache first. If not found, checks bounds, then runs the solver.
        """
        discrete_key = tuple(y)
        
        # 1. Check cache to avoid duplicate runs
        if discrete_key in self.cache:
            fobj = self.cache[discrete_key]
            self.cache_D_SDA[discrete_key] = fobj
            return fobj

        # 2. Check geometry/bounds
        if check_bounds(y):
            print(f'y = {y}')
            print('Violated geometry Fobj=1e5\n')
            fobj = 1e5
        else:
            # 3. Dynamically unpack variables for any length of y
            # Unpacks the first 3 to Ns, NFE, NFB and puts the rest into a list called NR
            Ns, NFE, NFB, *NR = y
            
            self.meshr.update_config(
                Ns=Ns,
                NFE=NFE,
                NFB=NFB,
                reactive_trays=NR  # Passes the dynamic list of reactive trays
            )
            
            sol = self.meshr.solve(solver="BARON")
            fobj = sol['Profit']
            self.eval_calls += self.meshr.flag_solver  # Increment only on actual solver calls

        # Save result to cache before returning
        self.cache[discrete_key] = fobj
        self.cache_D_SDA[discrete_key] = fobj
        return fobj

    def optimize(self, initial_y, cache=None):
        """
        Runs the Discrete Steepest Descent Algorithm (D-SDA).
        
        :param initial_y: List or tuple of initial variables [Ns, NFE, NFB, NR1, NR2...]
        :param cache: Optional dictionary to persist learned solutions across multiple optimizations
        :return: Dictionary containing the best solution, best objective value, and stats.
        """
        # Assign provided cache or initialize a new one
        if cache is not None:
            self.cache = cache
        else:
            self.cache = {}

        self.eval_calls = 0
        self.line_search_log = []
        start_time = time.perf_counter()

        y = list(initial_y)
        print(f"Starting configuration: {y}")

        # Evaluate the starting point
        fobj_best = self.evaluate(y)
        
        manager = CombinationManager()
        manager.history_set.update([tuple(y)])

        best_bool = True
        y_best = y

        while best_bool:
            best_bool = False
            
            # Generate list of combinatory neighbors (manager should support dynamic dimensions)
            batch = manager.generate_new_batch(y)

            # Evaluate neighbors
            fobj_list = [self.evaluate(y_d) for y_d in batch]

            fobj_challenger = min(fobj_list)
            challenger_idx = fobj_list.index(fobj_challenger)
            
            print(f"Challenger Fobj: {fobj_challenger:.4e} | Current Best Fobj: {fobj_best:.4e}")

            if fobj_challenger < fobj_best:
                y_old = y 
                fobj_best = fobj_challenger
                y = batch[challenger_idx]
                best_bool = True
                y_best = y

                # --- Line Search ---
                # Automatically handles dynamic length since it maps element-by-element
                d = [b - a for a, b in zip(y_old, y)]
                line_search = True
                self.line_search_log.append(f"first point line search: {y}")
                
                while line_search:
                    y_old = y
                    y_new = [a + b for a, b in zip(y, d)]
                    
                    self.line_search_log.append('linesearch start')
                    self.line_search_log.append(f"y = {y_new}; ")
                    self.line_search_log.append(f"d = {d};")

                    # Evaluate new point in line search (handles cache and bounds automatically)
                    fobj = self.evaluate(y_new)
                    manager.history_set.update([tuple(y_new)])
                    
                    print('line_search\n')
                    print(f"Current Best Y: {y_best}, Best Fobj: {fobj_best}, Calls: {self.eval_calls}")

                    if fobj < fobj_best:
                        fobj_best = fobj
                        y_best = y_new
                        y = y_new
                    else:
                        line_search = False

        print(f"Final Solution: {y_best}, Obj: {fobj_best:.4e}, Calls: {self.eval_calls}")
        
        end_time = time.perf_counter()
        exec_time = end_time - start_time

        return {
            'y_best': y_best,
            'fobj_best': fobj_best,
            'evaluations': self.eval_calls,
            'exec_time': exec_time,
            'line_search_log': self.line_search_log,
            'cache': self.cache  # Return cache so it can be passed to future runs
        }


# ==========================================
# Execution Example
# ==========================================
if __name__ == "__main__":
    # You can persist this dictionary if you run multiple times or save it to a pickle file
    shared_cache = {}
    
    # Instantiate the optimizer once
    optimizer = DiscreteOptimizer(max_stages=22)
    
    # User provides initial variables directly with arbitrary lengths
    # Example 1: 4 Variables
    # initial_y = [14, 7, 10, 7] 
    
    # Example 2: 7 Variables [Ns, NFE, NFB, NR1, NR2, NR3, NR4]
    initial_y = [7, 4, 4, 4, 5]
    
    # Run the optimization
    result = optimizer.optimize(initial_y=initial_y, cache=shared_cache)
    
    # Extract results
    y_best = result['y_best']
    fobj_best = result['fobj_best']
    fobj_calls = result['evaluations']
    time_spent = result['exec_time']
    logs = result['line_search_log']

    # Display final results
    print("\n--- Final Results ---")
    print(f"Execution time: {time_spent:.6f} seconds")
    print(f"Objective functions calls: {fobj_calls}")
    print(f"Best Discrete X found: {y_best}")
    print(f"Minimum Objective Value: {fobj_best:.4e}")

    # Write results to file
    with open("result/D-SDA_generic_optimization_results.txt", "a") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Run date: {datetime.now()}\n")
        f.write(f"Execution time: {time_spent:.6f} seconds\n")
        f.write(f"Objective functions calls: {fobj_calls}\n")
        f.write(f"Best Discrete X found: {y_best}\n")
        f.write(f"Minimum Objective Value: {fobj_best}\n")
        f.write("All values: \n")
        f.write(f"fobj_1 = {fobj_best:.4e}; y_1 = {y_best}; fobj_eval_1 = {fobj_calls}; initial_y_1 = {initial_y} \n")

    with open("result/all_resultsD-SDA_generic_optimization_results.txt", "a") as file:
        for txt in logs:
            file.write(f"{txt}\n")