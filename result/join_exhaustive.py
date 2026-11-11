import pandas as pd

# 1. Define the list of files to process
file_names = [
    'exhaustive_4D.csv', 
    'exhaustive_5D.csv', 
    'exhaustive_6D.csv', 
    'exhaustive_7D.csv'
]

# 2. Read each CSV and append to a list
dataframes = []
for file in file_names:
    # sep=';' handles the semicolon formatting from your example
    # If it happens to be tab-separated, change to sep='\t'
    df = pd.read_csv('result/' + file, sep=';')
    dataframes.append(df)

# 3. Combine them all into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# 4. Sort by the objective function (Profit)
# ascending=False puts the highest profit at the top. 
# Change to True if you are minimizing the objective function.
sorted_df = combined_df.sort_values(by='Profit', ascending=True)

# 5. Save to a new CSV file
# index=False prevents pandas from writing row numbers into the file
sorted_df.to_csv('result/exhaustive_combined_sorted.csv', sep=';', index=False)

print("Data successfully combined, sorted, and saved!")