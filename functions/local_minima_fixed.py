import pandas as pd
import itertools
from datetime import datetime
import os

def find_nd_local_minima_sparse(df, index_cols, value_col='Profit'):
    """Finds local minima using an optimized dictionary approach."""
    # 1. Build dictionary mapping coordinates to profit
    idx_tuples = tuple(df[index_cols].astype(int).itertuples(index=False, name=None))
    data_dict = dict(zip(idx_tuples, df[value_col].values))
    
    # 2. Generate neighborhood offsets
    n_dims = len(index_cols)
    offsets = list(itertools.product([-1, 0, 1], repeat=n_dims))
    offsets.remove((0,) * n_dims)
    
    results = []
    
    # 3. Search for minima
    for coords, value in data_dict.items():
        is_minima = True
        
        for offset in offsets:
            neighbor_coords = tuple(c + o for c, o in zip(coords, offset))
            
            # If neighbor exists and its profit is less than or equal to current value
            if neighbor_coords in data_dict:
                if value >= data_dict[neighbor_coords]:
                    is_minima = False
                    break # Stop checking neighbors early
                    
        if is_minima:
            results.append({
                'indices': coords,
                'value': value
            })
            
    return results

# --- MAIN EXECUTION LOOP ---

# Get today's date for filenames
today_str = datetime.now().strftime("%Y-%m-%d")
cols_to_exclude = {'Profit', 'Status', 'Dcol'}

for n in range(4, 8):
    file = f'result/exhaustive_{n}D.csv'
    
    if not os.path.exists(file):
        print(f"Warning: {file} not found. Skipping.")
        continue
        
    print(f"Processing {n}D...")
    
    # Read data and dynamically identify index columns
    df = pd.read_csv(file, sep=';').dropna(axis=1, how='all').dropna()
    index_cols = [col for col in df.columns if col not in cols_to_exclude]
    
    # Find the minima
    minima_results = find_nd_local_minima_sparse(df, index_cols, 'Profit')
    
    # Write to TXT file
    output_filename = f"result/local_minma_results_{n}D.txt"
    with open(output_filename, "a") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Local Minima Results for {n}D\n")
        f.write(f"Date: {today_str}\n")
        f.write(f"Total points analyzed: {len(df)}\n")
        f.write("=" * 50 + "\n")
        
        if len(minima_results) == 0:
            f.write("No local minima found.\n")
        else:
            for item in minima_results:
                f.write(f"Indices: {item['indices']} | Profit: {item['value']}\n")
                
    print(f"Successfully saved {len(minima_results)} minima to {output_filename}\n")