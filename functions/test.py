import pandas as pd

file = 'result/exhaustive_7D.csv'
df = pd.read_csv(file, sep=';').dropna(axis=1, how='all').dropna()

cols_to_exclude = {'Profit', 'Status', 'Dcol'}
index_cols = [col for col in df.columns if col not in cols_to_exclude]

# Find ALL rows that share the exact same index coordinates
duplicates_mask = df.duplicated(subset=index_cols, keep=False)
duplicates_df = df[duplicates_mask]

# Sort them by the coordinates so the duplicates are grouped together visually
duplicates_df = duplicates_df.sort_values(by=index_cols + ['Profit'])

print(f"Total rows in dataframe: {len(df)}")
print(f"Total duplicate rows found: {len(duplicates_df)}\n")

if len(duplicates_df) > 0:
    print("Here are the duplicate coordinate rows:")
    # Display all columns to see what is different (e.g., Profit, Status, Dcol)
    print(duplicates_df.head(20).to_string(index=False)) 
else:
    print("No duplicates found! The premise is false.")