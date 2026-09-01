import pandas as pd
import itertools

file = 'result/exhaustive_7D.csv'

# Read and clean data
df = pd.read_csv(file, sep=';').dropna(axis=1, how='all').dropna()

# Assuming df is already loaded and cleaned
index_cols = ['Ns', 'NFE', 'NFB', 'NR1', 'NR2', 'NR3', 'NR4']

# 1. Find the absolute best solution in the dataframe
best_idx = df['Profit'].idxmin()
best_row = df.loc[best_idx]
best_coords = tuple(best_row[index_cols].astype(int))
best_profit = best_row['Profit']

print(f"Absolute Best Solution: {best_coords} | Profit: {best_profit}")

# Check for duplicates of these exact coordinates
duplicates = df[(df[index_cols] == best_coords).all(axis=1)]
if len(duplicates) > 1:
    print(f"\nWARNING: Found {len(duplicates)} rows with coordinates {best_coords}!")
    print(duplicates)

# 2. Build the dictionary to simulate the sparse check
idx_tuples = tuple(df[index_cols].astype(int).itertuples(index=False, name=None))
data_dict = dict(zip(idx_tuples, df['Profit'].values))

# 3. Generate the 7D offsets
n_dims = len(index_cols)
offsets = list(itertools.product([-1, 0, 1], repeat=n_dims))
offsets.remove((0,) * n_dims)

# 4. Check all neighbors of the best solution
print("\n--- Checking Neighbors ---")
disqualifying_neighbors = []
existing_neighbors = []

for offset in offsets:
    # Calculate neighbor coordinate
    neighbor_coords = tuple(c + o for c, o in zip(best_coords, offset))
    
    # If the neighbor is in our dataset, check it
    if neighbor_coords in data_dict:
        neighbor_profit = data_dict[neighbor_coords]
        existing_neighbors.append((neighbor_coords, neighbor_profit))
        
        # If a neighbor is smaller or equal, it disqualifies our point
        if best_profit >= neighbor_profit:
            disqualifying_neighbors.append((neighbor_coords, neighbor_profit))

print(f"Total valid neighbors found in CSV: {len(existing_neighbors)}")

print("\n--- Disqualifying Neighbors ---")
if not disqualifying_neighbors:
    print("None! This point SHOULD be identified as a local minimum.")
else:
    for nc, np in disqualifying_neighbors:
        print(f"Disqualified by {nc} with profit {np}")