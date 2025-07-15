import pandas as pd

# Load the Excel file
path = "data/school_all.xlsx"
df = pd.read_excel(path, header=2)

# Print all unique school_id values
unique_ids = df['school_id'].unique()
print(sorted(unique_ids))
