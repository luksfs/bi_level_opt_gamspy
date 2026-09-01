import numpy as np
from scipy.ndimage import minimum_filter

def local_minima(df_new):
    arr = df_new.values  # the 2D matrix

    # Apply a local min filter with a 3x3 neighborhood
    local_min = (arr == minimum_filter(arr, size=3))  

    # Mask out edges or NaNs
    local_min = local_min & ~np.isnan(arr)

    # Extract coordinates
    coords = np.argwhere(local_min)

    for r, c in coords:
        print(f"Local minimum at Ns={df_new.index[r]}, NR1={df_new.columns[c]}, value={arr[r,c]}")
    
    return coords

def find_local_minima_scipy(df):
    """
    Finds all local minima using scipy.ndimage.minimum_filter.
    
    This is generally faster and cleaner than the shifted-array method.
    """
    
    # Get the underlying data
    data = df.values
    
    # 1. Define the 8-neighbor footprint (excluding the center)
    # This is a 3x3 matrix of True, with the center as False.
    # 
    footprint = np.ones((3, 3), dtype=bool)
    footprint[1, 1] = False
    
    # 2. Find the minimum of all 8 neighbors
    # We use mode='constant' and cval=np.inf to replicate the
    # "infinity padding" from the previous solution. This correctly
    # handles all edges and corners.
    min_of_neighbors = minimum_filter(
        data, 
        footprint=footprint, 
        mode='constant', 
        cval=np.inf
    )
    
    # 3. A cell is a local minimum if its value is
    #    strictly less than the minimum of all its neighbors.
    mask = data < min_of_neighbors
    count = mask.sum()

    # 4. Get the indices from the mask
    rows, cols = np.where(mask)

    # Print the count of min
    # print("Total n of min = {}".format(count))
    # Format the results nicely
    results = []
    for r, c in zip(rows, cols):
        results.append({
            'row': df.index[r],    # Use original DataFrame index
            'col': df.columns[c],  # Use original DataFrame columns
            'value': df.iloc[r, c]
        })
    
    return results, rows, cols, count


def find_nd_local_minima(data):
    """
    Finds all local minima in an N-dimensional NumPy array.
    
    A cell is a local minimum if it is strictly less than all its
    neighbors (including diagonals, in all N dimensions).
    """
    
    # 1. Get the number of dimensions
    n_dims = data.ndim
    
    # 2. Create the N-dimensional "Moore" neighborhood footprint.
    # For 2D, this is (3, 3). For 3D, this is (3, 3, 3), etc.
    # 
    footprint_shape = (3,) * n_dims
    footprint = np.ones(footprint_shape, dtype=bool)
    
    # 3. Set the center of the hypercube to False.
    # For 2D: (1, 1). For 3D: (1, 1, 1), etc.
    center_index = (1,) * n_dims
    footprint[center_index] = False
    
    # 4. Find the minimum of all neighbors for each cell.
    # mode='constant' and cval=np.inf correctly handles all
    # edges, corners, and hyper-corners in any dimension.
    min_of_neighbors = minimum_filter(
        data, 
        footprint=footprint, 
        mode='constant', 
        cval=np.inf
    )
    
    # 5. A cell is a local minimum if its value is
    #    strictly less than the minimum of all its neighbors.
    mask = data < min_of_neighbors
    
    # 6. Get the coordinates (indices) of the minima
    # np.where(mask) returns a tuple of N arrays
    coordinates = np.where(mask)
    
    # Format the results
    results = []
    # zip(*coordinates) iterates through the (dim0, dim1, ...) tuples
    for idx_tuple in zip(*coordinates):
        results.append({
            'indices': idx_tuple,
            'value': data[idx_tuple]
        })
        
    return results

import pandas as pd
import numpy as np
import itertools
from datetime import datetime

def find_nd_local_minima_sparse(df, index_cols, value_col='Profit'):
    """Finds local minima using a highly efficient dictionary approach."""
    # Create a dictionary mapping coordinate tuples to their Profit value
    idx_tuples = tuple(df[index_cols].astype(int).itertuples(index=False, name=None))
    profits = df[value_col].values
    data_dict = dict(zip(idx_tuples, profits))
    
    n_dims = len(index_cols)
    
    # Generate neighborhood offsets (-1, 0, 1) and remove the center
    offsets = list(itertools.product([-1, 0, 1], repeat=n_dims))
    offsets.remove((0,) * n_dims)
    
    results = []
    
    # Check each of your 9,000 data points
    for coords, value in data_dict.items():
        is_minima = True
        
        for offset in offsets:
            neighbor_coords = tuple(c + o for c, o in zip(coords, offset))
            
            # If the neighbor exists and is smaller/equal, this isn't a minimum
            if neighbor_coords in data_dict:
                if value >= data_dict[neighbor_coords]:
                    is_minima = False
                    break 
        
        if is_minima:
            results.append({
                'indices': coords,
                'value': value
            })
            
    return results

# --- MAIN EXECUTION ---

# Get today's date for the filenames
today_str = datetime.now().strftime("%Y-%m-%d")

for n in range(4, 8):
    file = f'result/exhaustive_{n}D.csv'
    
    try:
        # 1. Read and clean data
        df = pd.read_csv(file, sep=';').dropna(axis=1, how='all').dropna()
        
        # 2. Dynamically extract index columns
        cols_to_exclude = {'Profit', 'Status', 'Dcol'}
        index_cols = [col for col in df.columns if col not in cols_to_exclude]
        
        # 3. Find minima using the fast sparse method
        minima_results = find_nd_local_minima_sparse(df, index_cols, 'Profit')
        
        # 4. Save results to a text file
        output_filename = f"results_{n}D_{today_str}.txt"
        
        with open(output_filename, "w") as f:
            f.write(f"Local Minima Results for {n}D array\n")
            f.write(f"Date: {today_str}\n")
            f.write(f"Total data points processed: {len(df)}\n")
            f.write("=" * 50 + "\n")
            
            for item in minima_results:
                f.write(f"Indices: {item['indices']} | Profit: {item['value']}\n")
                
        print(f"Successfully processed {n}D and saved to {output_filename}")
        
    except FileNotFoundError:
        print(f"Warning: File {file} not found. Skipping.")




# import pandas as pd
# import numpy as np
# from datetime import datetime

# for n in range(4, 8):
#     file = f'result/exhaustive_{n}D.csv'
    
#     # Read and clean the dataframe
#     df = pd.read_csv(file, sep=';')
#     df = df.dropna(axis=1, how='all').dropna()
    
#     # 1. Dynamically define index columns by EXCLUDING unwanted ones
#     cols_to_exclude = {'Profit', 'Status', 'Dcol'}
#     index_cols = [col for col in df.columns if col not in cols_to_exclude]
    
#     # NOTE: If your index columns are always exactly the first 'n' columns,
#     # you could skip the exclusion list and just use:
#     # index_cols = df.columns[:n]
    
#     # 2. Calculate the shape of the ND array
#     max_indices = df[index_cols].max().astype(int) + 1
#     shape_tuple = tuple(max_indices)
    
#     # 3. Initialize the ND array
#     # array_nd = np.full(shape_tuple, np.nan)
#     array_nd = np.full(shape_tuple, np.inf, dtype=np.float32)
    
#     # 4. Fill the array efficiently (Vectorization)
#     idx_tuple = tuple(df[index_cols].astype(int).values.T)
#     profit_values = df['Profit'].values
    
#     # Assign ALL rows to the ND array in one operation
#     array_nd[idx_tuple] = profit_values

#     # Test the output
#     # print(find_nd_local_minima(array_nd))

#     # Run your function and store the result
#     minima_results = find_nd_local_minima(array_nd)
#     print(minima_results)

#     # Get today's date (e.g., '2026-08-27')
#     today_str = datetime.now().strftime("%Y-%m-%d")

#     # Create a dynamic filename (e.g., 'results_4D_2026-08-27.txt')
#     output_filename = f"result/local_minima_results_{n}D_{today_str}.txt"

#     # Write the results to the .txt file
#     with open(output_filename, "w") as file:
#         # Write a header
#         file.write(f"Local Minima Results for {n}D array\n")
#         file.write(f"Date: {today_str}\n")
#         file.write("=" * 50 + "\n")
        
#         # Iterate through the returned list of dictionaries
#         for item in minima_results:
#             indices_str = str(item['indices'])
#             value_str = str(item['value'])
            
#             # Write each result on a new line
#             file.write(f"Indices: {indices_str} | Value: {value_str}\n")


# import pandas as pd

# import numpy as np

# df = pd.read_csv('result/exhaustive_5D.csv',sep=';')
# df = df.drop(columns=['NR3', 'NR4'])
# df = df.dropna()

# # Find the maximum value for each dimension
# max_Ns = df['Ns'].max()
# max_NFE = df['NFE'].max()
# max_NFB = df['NFB'].max()
# max_NR1 = df['NR1'].max()
# max_NR2 = df['NR2'].max()
# # max_NR3 = df['NR3'].max()

# # Create array with size to fit the maximum indices (+1 because indices start at 0)
# array_6d = np.full(
#     (max_Ns + 1, max_NFE + 1, max_NFB + 1, max_NR1 + 1, max_NR2 + 1, ), np.nan)



# # Fill the array directly with your values
# for _, row in df.iterrows():
#     array_6d[
#         row['Ns'], row['NFE'], 
#         row['NFB'], row['NR1'],
#         row['NR2']
#         ] = row['Profit']

# # Now you can access directly with your original indices!
# # value = array_6d[6, 1, 3, 1]
# # print(value)  # Should print 0.0188003265573655
# # array_6d[14,2,4,2] = 0.0017
# # array_6d[12,2,4,2] = 0.0017
# print(find_nd_local_minima(array_6d))