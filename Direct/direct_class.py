# another try with a class
# import gamspy
# import gamspy as gp
# import gamspy.math as gmath
# from cost import Cost
# import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
from gamspy_model.meshr_class import ReactiveDistillationModel

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

    def evaluate_4D(self, x_c):
        """The continuous wrapper method passed to SciPy."""
        # Round to integers
        # x_continuous[0] is in range [5.5, 20.4]
        Ns_c, NFE_c, NFB_c, NR1_c = x_c
        # print(x_c)

        Ns = int(np.round(Ns_c))
        
        NFE = int( np.round( 2 + NFE_c * (Ns - 4)) )
        NFB = int( np.round( NFE + NFB_c * (Ns - 2 - NFE) ) )
        NR1 = int( np.round( 2 + NR1_c * (Ns - 4) ) )

        x_discrete = [Ns, NFE, NFB, NR1]
        reactive_trays = [NR1]
            
        # Cache Check
        discrete_key = tuple(x_discrete)
        if discrete_key in self.cache:
            base_obj = self.cache[discrete_key]
        else:
            # Execute the real objective and save it
            self.meshr.update_config(Ns, NFE, NFB, reactive_trays)
            sol = self.meshr.solve(solver="BARON")
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
                self.counter +=1
            else:
                print(
                    'Failed solution: '
                    'NFE = {:d}, '
                    'NFB = {:d}, '
                    'NR1 = {:d}, '.format(NFE, NFB, NR1)
                )
                base_obj = 1e5
                
            self.cache[discrete_key] = base_obj
        return base_obj #+ distance_penalty

    def evaluate_5D(self, x_c):
        """The continuous wrapper method passed to SciPy."""
        # Round to integers
        # x_continuous[0] is in range [5.5, 20.4]
        Ns_c, NFE_c, NFB_c, NR1_c, NR2_c = x_c
        # print(x_c)

        Ns = int(np.round(Ns_c))
        
        # NFE = int( np.round( 1 + NFE_c * (Ns - 3)) )
        # NFB = int( np.round( NFE + NFB_c * (Ns - 2 - NFE) ) )
        # NR1 = int( np.round( 1 + NR1_c * (Ns - 4) ) )
        # NR2 = int( np.round( NR1 + 1 + NR2_c * (Ns - 3 - NR1) ) )

        NFE = int( np.round( 2 + NFE_c * (Ns - 4)) )
        NFB = int( np.round( NFE + NFB_c * (Ns - 2 - NFE) ) )
        NR1 = int( np.round( 2 + NR1_c * (Ns - 5) ) )
        NR2 = int( np.round( NR1 + 1 + NR2_c * (Ns - 3 - NR1) ) )

        x_discrete = [Ns, NFE, NFB, NR1, NR2]
        reactive_trays = [NR1, NR2]
            
        # Cache Check
        discrete_key = tuple(x_discrete)
        if discrete_key in self.cache:
            base_obj = self.cache[discrete_key]
        else:
            # Execute the real objective and save it
            self.meshr.update_config(Ns, NFE, NFB, reactive_trays)
            sol = self.meshr.solve(solver="BARON")
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
                self.counter +=1
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
        return base_obj #+ distance_penalty

    def evaluate_6D(self, x_c):
        """The continuous wrapper method passed to SciPy."""
        # Round to integers
        # x_continuous[0] is in range [5.5, 20.4]
        Ns_c, NFE_c, NFB_c, NR1_c, NR2_c, NR3_c = x_c
        # print(x_c)

        Ns = int(np.round(Ns_c))
        
        # NFE = int( np.round( 1 + NFE_c * (Ns - 3)) )
        # NFB = int( np.round( NFE + NFB_c * (Ns - 2 - NFE) ) )
        # NR1 = int( np.round( 1 + NR1_c * (Ns - 5) ) )
        # NR2 = int( np.round( NR1 + 1 + NR2_c * (Ns - 4 - NR1) ) )
        # NR3 = int( np.round( NR2 + 1 + NR3_c * (Ns - 3 - NR2) ) )
        NFE = int( np.round( 2 + NFE_c * (Ns - 4)) )
        NFB = int( np.round( NFE + NFB_c * (Ns - 2 - NFE) ) )
        NR1 = int( np.round( 2 + NR1_c * (Ns - 6) ) )
        NR2 = int( np.round( NR1 + 1 + NR2_c * (Ns - 4 - NR1) ) )
        NR3 = int( np.round( NR2 + 1 + NR3_c * (Ns - 3 - NR2) ) )

        x_discrete = [Ns, NFE, NFB, NR1, NR2, NR3]
        reactive_trays = [NR1, NR2, NR3]
            
        # Cache Check
        discrete_key = tuple(x_discrete)
        if discrete_key in self.cache:
            base_obj = self.cache[discrete_key]
        else:
            # Execute the real objective and save it
            self.meshr.update_config(Ns, NFE, NFB, reactive_trays)
            sol = self.meshr.solve(solver="BARON")
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
                self.counter +=1
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
        return base_obj #+ distance_penalty

    def evaluate_7D(self, x_c):
        """The continuous wrapper method passed to SciPy."""
        # Round to integers
        # x_continuous[0] is in range [5.5, 20.4]
        Ns_c, NFE_c, NFB_c, NR1_c, NR2_c, NR3_c, NR4_c = x_c
        # print(x_c)

        Ns = int(np.round(Ns_c))
        
        # NFE = int( np.round( 1 + NFE_c * (Ns - 3)) )
        # NFB = int( np.round( NFE + NFB_c * (Ns - 2 - NFE) ) )
        # NR1 = int( np.round( 1 + NR1_c * (Ns - 6) ) )
        # NR2 = int( np.round( NR1 + 1 + NR2_c * (Ns - 5 - NR1) ) )
        # NR3 = int( np.round( NR2 + 1 + NR3_c * (Ns - 4 - NR2) ) )
        # NR4 = int( np.round( NR3 + 1 + NR4_c * (Ns - 3 - NR3) ) )

        NFE = int( np.round( 2 + NFE_c * (Ns - 4)) )
        NFB = int( np.round( NFE + NFB_c * (Ns - 2 - NFE) ) )
        NR1 = int( np.round( 2 + NR1_c * (Ns - 7) ) )
        NR2 = int( np.round( NR1 + 1 + NR2_c * (Ns - 5 - NR1) ) )
        NR3 = int( np.round( NR2 + 1 + NR3_c * (Ns - 4 - NR2) ) )
        NR4 = int( np.round( NR3 + 1 + NR4_c * (Ns - 3 - NR3) ) )

        x_discrete = [Ns, NFE, NFB, NR1, NR2, NR3, NR4]
        reactive_trays = [NR1, NR2, NR3, NR4]
            
        # Cache Check
        discrete_key = tuple(x_discrete)
        if discrete_key in self.cache:
            base_obj = self.cache[discrete_key]
        else:
            # Execute the real objective and save it
            self.meshr.update_config(Ns, NFE, NFB, reactive_trays)
            sol = self.meshr.solve(solver="BARON")
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
                self.counter +=1
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