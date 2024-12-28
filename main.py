import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('transactions.csv')

# Print the first few rows
print(df.head())

print("Data Info:")
print(df.info())

print("\nSummary Statistics:")
print(df.describe())