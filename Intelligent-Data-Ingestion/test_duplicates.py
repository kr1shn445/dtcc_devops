
import pandas as pd
from src.validation.csv_validator import detect_duplicates

df = pd.read_csv("data/sample/transactions.csv")

# Add a duplicate transaction for testing
df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

result = detect_duplicates(df)

print("Duplicate Detection Results")
print("----------------------------")
print("Total Records:", len(df))
print("Duplicate Records:", result["duplicate_count"])
print("\nDetected Duplicates:")
print(result["duplicates"])
