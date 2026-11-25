import os
import time
from datetime import datetime
from functions.comb_manager import CombinationManager
from functions.invalid_check import check_bounds
from gamspy_model.meshr_class import ReactiveDistillationModel


class DiscreteOptimizer:
    def __init__(self, max_stages=22, conopt_time_limit=15, baron_time_limit=160, meshr=None):

        """Initialize the MESHR superstructure model and evaluation trackers."""
        self.meshr = meshr if meshr is not None else ReactiveDistillationModel(max_stages=max_stages)
        self._owns_meshr = meshr is None
        # self.meshr = ReactiveDistillationModel(max_stages=max_stages)
        self.conopt_time_limit = conopt_time_limit
        self.baron_time_limit = baron_time_limit
        self.eval_calls = 0
        self.cache = {}
        self.cache_D_SDA = {}
        self.line_search_log = []

    def close(self):
        """Close the GAMSPy container and remove temporary GAMS files."""
        if hasattr(self, "meshr") and hasattr(self.meshr, "m"):
            self.meshr.m.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def evaluate(self, y):
        """
        Evaluates the objective function for any 4D-7D vector [Ns, NFE, NFB, NR1, ...].
        Checks cache and bounds first, then runs CONOPT warm-start -> BARON global solve.
        """
        y_int = [int(v) for v in y]
        discrete_key = tuple(y_int)

        # 1. Check cache to avoid duplicate runs
        if discrete_key in self.cache:
            fobj = self.cache[discrete_key]
            self.cache_D_SDA[discrete_key] = fobj
            return fobj

        # 2. Check geometry/bounds before touching the solver
        if check_bounds(y_int):
            print(f"y = {y_int}")
            print("Violated geometry Fobj=1e5\n")
            fobj = 1e5
        else:
            Ns, NFE, NFB, *NR = y_int

            # Reset variable levels so previous solves do not contaminate the warm-start
            self.meshr.reset_levels()
            self.meshr.update_config(
                Ns=Ns,
                NFE=NFE,
                NFB=NFB,
                reactive_trays=NR,
            )

            # 3a. Fast CONOPT warm-start
            ws = self.meshr.solve(
                solver="CONOPT",
                threads=1,
                time_limit=self.conopt_time_limit,
            )

            if self.meshr.flag_solver == 0:
                # Discrete bounds violated inside meshr.solve(); skip BARON
                fobj = 1e5
            else:
                if getattr(ws["Status"], "value", -1) not in (1, 2):
                    # Clear diverged CONOPT iterate before handing off to BARON
                    self.meshr.reset_levels()
                    self.meshr._init_temp_and_hr()

                # 3b. Global solve with BARON
                sol = self.meshr.solve(
                    solver="BARON",
                    threads=1,
                    time_limit=self.baron_time_limit,
                )
                self.eval_calls += self.meshr.flag_solver

                if getattr(sol["Status"], "value", -1) in (1, 2):
                    fobj = float(sol["Profit"])
                else:
                    fobj = 1e5

        # Save result to caches before returning
        self.cache[discrete_key] = fobj
        self.cache_D_SDA[discrete_key] = fobj
        return fobj

    def optimize(self, initial_y, cache=None):
        """
        Runs the Discrete Steepest Descent Algorithm (D-SDA).

        :param initial_y: List or tuple of initial variables [Ns, NFE, NFB, NR1, NR2, ...]
        :param cache: Optional dictionary to persist learned solutions across optimizations
        :return: Dictionary containing the best solution, best objective value, and stats.
        """
        self.cache = cache if cache is not None else {}
        self.cache_D_SDA = {}
        self.eval_calls = 0
        self.line_search_log = []
        start_time = time.perf_counter()

        y = [int(v) for v in initial_y]
        print(f"Starting configuration: {y}")

        # Evaluate the starting point
        fobj_best = self.evaluate(y)

        manager = CombinationManager()
        manager.history_set.update([tuple(y)])

        best_bool = True
        y_best = list(y)

        while best_bool:
            best_bool = False

            # Generate list of combinatory neighbors
            batch = manager.generate_new_batch(y)
            if not batch:
                break

            # Evaluate neighbors
            fobj_list = [self.evaluate(y_d) for y_d in batch]

            fobj_challenger = min(fobj_list)
            challenger_idx = fobj_list.index(fobj_challenger)

            print(f"Challenger Fobj: {fobj_challenger:.6e} | Current Best Fobj: {fobj_best:.6e}")

            if fobj_challenger < fobj_best:
                y_old = y
                fobj_best = fobj_challenger
                y = [int(v) for v in batch[challenger_idx]]
                best_bool = True
                y_best = list(y)

                # --- Line Search ---
                d = [b - a for a, b in zip(y_old, y)]
                line_search = True
                self.line_search_log.append(f"first point line search: {y}")

                while line_search:
                    y_new = [a + b for a, b in zip(y, d)]

                    self.line_search_log.append("linesearch start")
                    self.line_search_log.append(f"y = {y_new}; ")
                    self.line_search_log.append(f"d = {d};")

                    # Evaluate new point (handles cache and bounds automatically)
                    fobj = self.evaluate(y_new)
                    manager.history_set.update([tuple(y_new)])

                    print("line_search\n")
                    print(f"Current Best Y: {y_best}, Best Fobj: {fobj_best:.6e}, Calls: {self.eval_calls}")

                    if fobj < fobj_best:
                        fobj_best = fobj
                        y_best = list(y_new)
                        y = y_new
                    else:
                        line_search = False

        print(f"Final Solution: {y_best}, Obj: {fobj_best:.6e} (${fobj_best * 1e6:,.2f}/yr), Calls: {self.eval_calls}")

        exec_time = time.perf_counter() - start_time

        return {
            "y_best": y_best,
            "fobj_best": fobj_best,
            "evaluations": self.eval_calls,
            "exec_time": exec_time,
            "line_search_log": self.line_search_log,
            "cache": self.cache,
            "cache_D_SDA": self.cache_D_SDA,
        }


# ==========================================
# Execution Example
# ==========================================
if __name__ == "__main__":
    os.makedirs("result", exist_ok=True)
    shared_cache = {}
    initial_y = [7, 4, 4, 4, 5]

    with DiscreteOptimizer(max_stages=22) as optimizer:
        result = optimizer.optimize(initial_y=initial_y, cache=shared_cache)

    y_best = result["y_best"]
    fobj_best = result["fobj_best"]
    fobj_calls = result["evaluations"]
    time_spent = result["exec_time"]
    logs = result["line_search_log"]

    print("\n--- Final Results ---")
    print(f"Execution time: {time_spent:.6f} seconds")
    print(f"Objective function calls: {fobj_calls}")
    print(f"Best Discrete X found: {y_best}")
    print(f"Minimum Objective Value: {fobj_best:.6e} (${fobj_best * 1e6:,.2f}/yr)")

    with open("result/D-SDA_generic_optimization_results.txt", "a") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Run date: {datetime.now()}\n")
        f.write(f"Execution time: {time_spent:.6f} seconds\n")
        f.write(f"Objective functions calls: {fobj_calls}\n")
        f.write(f"Best Discrete X found: {y_best}\n")
        f.write(f"Minimum Objective Value: {fobj_best:.6e}\n")
        f.write("All values:\n")
        f.write(
            f"fobj_1 = {fobj_best:.6e}; y_1 = {y_best}; "
            f"fobj_eval_1 = {fobj_calls}; initial_y_1 = {initial_y}\n"
        )

    with open("result/all_resultsD-SDA_generic_optimization_results.txt", "a") as file:
        for txt in logs:
            file.write(f"{txt}\n")