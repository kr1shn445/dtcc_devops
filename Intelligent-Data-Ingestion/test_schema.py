
import pandas as pd
from src.validation.schema import validate_schema

file_path = "data/downloaded/transactions.csv"

df = pd.read_csv(file_path)

result = validate_schema(df)

print("Schema and Data Type Validation")
print("--------------------------------")
print("Expected Columns:", 6)
print("Actual Columns:", len(df.columns))

if result["is_valid"]:
    print("Schema Status: VALID")
    print("All required columns and data types are correct.")
else:
    print("Schema Status: INVALID")
    for error in result["errors"]:
        print("Error:", error)
