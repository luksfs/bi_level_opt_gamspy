# another try with a class
# import gamspy
# import gamspy as gp
# import gamspy.math as gmath
# from cost import Cost
# import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
from gamspy_model.meshr_class import ReactiveDistillationModel
# from gamspy_model.meshr_class_without_cat_res import ReactiveDistillationModel

# 1. We keep the custom exception outside the class (standard Python practice)
class EarlyStopException(Exception):
    """Raised to cleanly break out of SciPy's internal loop."""
    pass

# 2. The Optimizer Class
class DiscreteDirectWrapper:
    def __init__(self, patience=200):
        # Store the actual objective function
        # self.discrete_objective = discrete_objective_func
        self.patience = patience
        
        # State tracking (No more globals!)
        self.cache = {}
        self.best_discrete_so_far = None
        self.stagnant_iterations = 0
        self.final_x = None
        self.final_fun = None
        self.counter = 0
        # 1. Initialize the class (Builds the 22-stage matrix once)
        self.meshr = ReactiveDistillationModel(max_stages=22)
        self.max_Ns=22
        self.penalty_weight = 1e-4

    def map_discrete_variables_penalty(self, x_c, max_Ns=22):
        """
        Generalized mapping for [Ns, NFE, NFB, NR1, ..., NRk]
        Assumes x_c[0] is bounded like [5.0, 23.0] and the rest [0.0, 1.0].
        Returns the mapped discrete tuple and the distance penalty to avoid plateaus.
        """
        n_vars = len(x_c)
        k_nr = n_vars - 3  # Number of NR variables
        total_distance = 0.0

        # Map Ns
        Ns_idx = int(np.floor(x_c[0]))
        Ns = min(Ns_idx, max_Ns)
        
        # Distance from center of Ns bin (center is Ns + 0.5)
        total_distance += abs(x_c[0] - (Ns + 0.5))

        # Map NFE
        min_NFE = 2
        max_NFE = Ns - 2
        options_NFE = max_NFE - min_NFE + 1
        
        idx_NFE = int(np.floor(x_c[1] * options_NFE))
        idx_NFE = min(idx_NFE, options_NFE - 1)  # Clamp for x=1.0 edge case
        NFE = min_NFE + idx_NFE
        
        position_NFE = x_c[1] * options_NFE
        total_distance += abs(position_NFE - (idx_NFE + 0.5))
        
        # Map NFB
        min_NFB = NFE
        max_NFB = Ns - 2
        options_NFB = max_NFB - min_NFB + 1
        
        idx_NFB = int(np.floor(x_c[2] * options_NFB))
        idx_NFB = min(idx_NFB, options_NFB - 1)
        NFB = min_NFB + idx_NFB
        
        position_NFB = x_c[2] * options_NFB
        total_distance += abs(position_NFB - (idx_NFB + 0.5))
        
        # Map NR1 through NRk dynamically
        mapped_vars = [Ns, NFE, NFB]
        last_NR = None
        
        for i in range(k_nr):
            c_val = x_c[3 + i]  # The continuous [0,1] input for this specific NR
            current_step = i + 1  # 1-based index (1 to k_nr)
            
            # Minimum depends on the previous NR
            if current_step == 1:
                min_NR = 2
            else:
                min_NR = last_NR + 1
                
            # Maximum leaves exactly enough room for the remaining NR variables
            # e.g., if total is 4, NR4 max is Ns-2, NR3 max is Ns-3, NR2 max is Ns-4, etc.
            max_NR = Ns - 2 - (k_nr - current_step)
            
            # Map using the unbiased floor logic
            options_NR = max_NR - min_NR + 1
            idx_NR = int(np.floor(c_val * options_NR))
            idx_NR = min(idx_NR, options_NR - 1)
            NR = min_NR + idx_NR
            
            position_NR = c_val * options_NR
            total_distance += abs(position_NR - (idx_NR + 0.5))
            
            mapped_vars.append(NR)
            last_NR = NR
        
        return tuple(mapped_vars), total_distance

    def map_discrete_variables(self, x_c, max_Ns=22):
        """
        Generalized mapping for [Ns, NFE, NFB, NR1, ..., NRk]
        Assumes x_c[0] is bounded like [5.0, 23.0] and the rest are [0.0, 1.0].
        """
        n_vars = len(x_c)
        k_nr = n_vars - 3  # Number of NR variables (e.g., 4 for a 7-var array)
        
        # 1. Map Ns
        Ns = int(np.floor(x_c[0]))
        Ns = min(Ns, max_Ns)  # Clamp just in case the optimizer tests the absolute upper bound
        
        # 2. Map NFE
        min_NFE = 2
        max_NFE = Ns - 2
        options_NFE = max_NFE - min_NFE + 1
        NFE = min_NFE + int(np.floor(x_c[1] * options_NFE))
        NFE = min(NFE, max_NFE) # Clamp for x=1.0 edge case
        
        # 3. Map NFB
        min_NFB = NFE
        max_NFB = Ns - 2
        options_NFB = max_NFB - min_NFB + 1
        NFB = min_NFB + int(np.floor(x_c[2] * options_NFB))
        NFB = min(NFB, max_NFB)
        
        # 4. Map NR1 through NRk dynamically
        mapped_vars = [Ns, NFE, NFB]
        last_NR = None
        
        for i in range(k_nr):
            c_val = x_c[3 + i] # The continuous [0,1] input for this specific NR
            current_step = i + 1  # 1-based index (1 to k_nr)
            
            # Minimum depends on the previous NR
            if current_step == 1:
                min_NR = 2
            else:
                min_NR = last_NR + 1
                
            # Maximum leaves exactly enough room for the remaining NR variables
            # e.g., if total is 4, NR4 max is Ns-2, NR3 max is Ns-3, NR2 max is Ns-4, etc.
            max_NR = Ns - 2 - (k_nr - current_step)
            
            # Map using the unbiased floor logic
            options_NR = max_NR - min_NR + 1
            NR = min_NR + int(np.floor(c_val * options_NR))
            NR = min(NR, max_NR)
            
            mapped_vars.append(NR)
            last_NR = NR
        total_distance = 0
        return tuple(mapped_vars), total_distance


    def evaluate_4D(self, x_c):
        """The connuous wrapper method passed to SciPy."""

        mapped_vars, total_distance = self.map_discrete_variables(x_c, max_Ns=self.max_Ns)

        [Ns, NFE, NFB, NR1]= mapped_vars

        x_discrete = [Ns, NFE, NFB, NR1]
        reactive_trays = [NR1]
            
        # Cache Check
        discrete_key = tuple(x_discrete)
        if discrete_key in self.cache:
            base_obj = self.cache[discrete_key]
            return base_obj
        else:
            # Execute the real objective and save it
            self.meshr.update_config(Ns, NFE, NFB, reactive_trays)
            sol = self.meshr.solve(solver="BARON")
            self.counter +=self.meshr.flag_solver
            print('Fobj call iter = {:d}'.format(self.counter))
            if sol['Status'].value == 1 or sol['Status'].value == 2:
                base_obj = sol['Profit']
                # Fixed the format specifier, fixed typo (Fobj), 
                # and added 'base_obj' to fill the 6th placeholder.
                print(
                    'NFE = {:d}, '
                    'NFB = {:d}, '
                    'NR1 = {:d},\n'
                    'Fobj = {:.4f}'.format(NFE, NFB, NR1, base_obj)
                )
                
            else:
                print(
                    'Failed solution: '
                    'NFE = {:d}, '
                    'NFB = {:d}, '
                    'NR1 = {:d}, '.format(NFE, NFB, NR1)
                )
                base_obj = 1e5
                
            self.cache[discrete_key] = base_obj

            distance_penalty = total_distance*self.penalty_weight
        return base_obj #+ distance_penalty

    def evaluate_5D(self, x_c):
        """The continuous wrapper method passed to SciPy."""

        mapped_vars, total_distance = self.map_discrete_variables(x_c, max_Ns=self.max_Ns)

        [Ns, NFE, NFB, NR1, NR2]= mapped_vars

        x_discrete = [Ns, NFE, NFB, NR1, NR2]
        reactive_trays = [NR1, NR2]
            
        # Cache Check
        discrete_key = tuple(x_discrete)
        if discrete_key in self.cache:
            base_obj = self.cache[discrete_key]
            return base_obj
        else:
            # Execute the real objective and save it
            self.meshr.update_config(Ns, NFE, NFB, reactive_trays)
            sol = self.meshr.solve(solver="BARON")
            # base_obj = 1e5
            self.counter +=self.meshr.flag_solver
            print('Fobj call iter = {:d}'.format(self.counter))
            if sol['Status'].value == 1 or sol['Status'].value == 2:
                base_obj = sol['Profit']
                # Fixed the format specifier, fixed typo (Fobj), 
                # and added 'base_obj' to fill the 6th placeholder.
                print(
                    'NFE = {:d}, '
                    'NFB = {:d}, '
                    'NR1 = {:d}, '
                    'NR2 = {:d},\n'
                    'Fobj = {:.4f}'.format(NFE, NFB, NR1, NR2, base_obj)
                )
                # self.counter +=1
            else:
                print(
                    'Failed solution: '
                    'NFE = {:d}, '
                    'NFB = {:d}, '
                    'NR1 = {:d}, '
                    'NR2 = {:d}, '.format(NFE, NFB, NR1, NR2)
                )
                base_obj = 1e5
                    
            self.cache[discrete_key] = base_obj
            distance_penalty = total_distance*self.penalty_weight
        return base_obj #+ distance_penalty

    def evaluate_6D(self, x_c):
        """The continuous wrapper method passed to SciPy."""
        # Round to integers
        # x_continuous[0] is in range [5.5, 20.4]
        # Ns_c, NFE_c, NFB_c, NR1_c, NR2_c, NR3_c, NR4_c = x_c

        mapped_vars, total_distance = self.map_discrete_variables(x_c, max_Ns=self.max_Ns)

        [Ns, NFE, NFB, NR1, NR2, NR3]= mapped_vars

        x_discrete = [Ns, NFE, NFB, NR1, NR2, NR3]
        reactive_trays = [NR1, NR2, NR3]
            
        # Cache Check
        discrete_key = tuple(x_discrete)
        if discrete_key in self.cache:
            base_obj = self.cache[discrete_key]
            return base_obj
        else:
            # Execute the real objective and save it
            self.meshr.update_config(Ns, NFE, NFB, reactive_trays)
            sol = self.meshr.solve(solver="BARON")
            self.counter +=self.meshr.flag_solver
            print('Fobj call iter = {:d}'.format(self.counter))
            if sol['Status'].value == 1 or sol['Status'].value == 2:
                base_obj = sol['Profit']
                
                # Fixed the format specifier, fixed typo (Fobj), 
                # and added 'base_obj' to fill the 6th placeholder.
                print(
                    'NFE = {:d}, '
                    'NFB = {:d}, '
                    'NR1 = {:d}, '
                    'NR2 = {:d}, '
                    'NR3 = {:d},\n'
                    'Fobj = {:.4f}'.format(NFE, NFB, NR1, NR2, NR3, base_obj)
                )
            else:
                print(
                    'Failed solution: '
                    'NFE = {:d}, '
                    'NFB = {:d}, '
                    'NR1 = {:d}, '
                    'NR2 = {:d}, '
                    'NR3 = {:d},'.format(NFE, NFB, NR1, NR2, NR3)
                )
                base_obj = 1e5
                
            self.cache[discrete_key] = base_obj
            print('xc = ', x_c)
            distance_penalty = total_distance*self.penalty_weight
        return base_obj #+ distance_penalty

    def evaluate_7D(self, x_c):
        """The continuous wrapper method passed to SciPy."""
        # Round to integers
        # x_continuous[0] is in range [5.5, 20.4]
        # Ns_c, NFE_c, NFB_c, NR1_c, NR2_c, NR3_c, NR4_c = x_c

        mapped_vars, total_distance = self.map_discrete_variables(x_c, max_Ns=self.max_Ns)

        [Ns, NFE, NFB, NR1, NR2, NR3, NR4]= mapped_vars

        x_discrete = [Ns, NFE, NFB, NR1, NR2, NR3, NR4]
        reactive_trays = [NR1, NR2, NR3, NR4]
            
        # Cache Check
        discrete_key = tuple(x_discrete)
        if discrete_key in self.cache:
            base_obj = self.cache[discrete_key]
            return base_obj
        else:
            # Execute the real objective and save it
            self.meshr.update_config(Ns, NFE, NFB, reactive_trays)
            sol = self.meshr.solve(solver="BARON")
            self.counter +=self.meshr.flag_solver
            print('Fobj call iter = {:d}'.format(self.counter))
            if sol['Status'].value == 1 or sol['Status'].value == 2:
                base_obj = sol['Profit']
                
                # Fixed the format specifier, fixed typo (Fobj), 
                # and added 'base_obj' to fill the 6th placeholder.
                print(
                    'NFE = {:d}, '
                    'NFB = {:d}, '
                    'NR1 = {:d}, '
                    'NR2 = {:d}, '
                    'NR3 = {:d}, '
                    'NR4 = {:d},\n'
                    'Fobj = {:.4f}'.format(NFE, NFB, NR1, NR2, NR3, NR4, base_obj)
                )
            else:
                print(
                    'Failed solution: '
                    'NFE = {:d}, '
                    'NFB = {:d}, '
                    'NR1 = {:d}, '
                    'NR2 = {:d}, '
                    'NR3 = {:d}, '
                    'NR4 = {:d},'.format(NFE, NFB, NR1, NR2, NR3, NR4)
                )
                base_obj = 1e5
                
            self.cache[discrete_key] = base_obj
            print('xc = ', x_c)
            distance_penalty = total_distance*self.penalty_weight
        return base_obj #+ distance_penalty
    
    def callback(self, xk):
        """The callback method passed to SciPy."""
        current_best_discrete = tuple(np.round(xk).astype(int))
        
        if current_best_discrete == self.best_discrete_so_far:
            self.stagnant_iterations += 1
        else:
            self.best_discrete_so_far = current_best_discrete
            self.stagnant_iterations = 0 
            
        if self.stagnant_iterations >= self.patience:
            # Save the final results to the class instance before crashing
            self.final_x = self.best_discrete_so_far
            self.final_fun = self.cache[self.best_discrete_so_far]
            raise EarlyStopException("Discrete solution converged!")
    
def process_gdx_data(gdx_container):
    # 1. Load Data
    # (No need for deep=True unless you plan to modify the original gdx object elsewhere)
    df = gdx_container.data['profit_obj'].records.copy()

    # 2. Dynamic Column Naming
    # Define the expected order of index columns (excluding 'obj')
    possible_indices = ['Ns', 'NFE', 'NFB', 'NR1', 'NR2', 'NR3']

    # Calculate how many index columns this specific dataframe has
    # (Total columns - 1 for the 'obj' column)
    num_index_cols = df.shape[1] - 1

    # Slice the name list to match the actual data width
    current_indices = possible_indices[:num_index_cols]
    df.columns = current_indices + ['obj']

    # 3. Efficient Casting & Adjustment
    # Identify columns that need 0-based indexing (Everything except 'Ns' and 'obj')
    # We use set intersection to find which 'N...' columns are actually present
    cols_to_adjust = [col for col in current_indices if col != 'Ns']

    # Cast all indices to int32 in one go
    df[current_indices] = df[current_indices].astype('int32')

    # Vectorized subtraction: Update all relevant columns at once
    # This is much faster than doing df['NFE'] = ..., df['NR1'] = ... separately
    df[cols_to_adjust] -= 1

    # 4. Filter
    # Check for -1 only in the index columns (more efficient than checking 'obj' too)
    # df = df[~(df[current_indices] == -1).any(axis=1)]
    df = df[~(df == -1).any(axis=1)]

    return df

# ---------------------------------------------------------
# How to use the class
# ---------------------------------------------------------
# Define your actual solver function somewhere
# def my_expensive_solver(x_discrete, df):
#     return (np.sum(x_discrete) - 25)**2