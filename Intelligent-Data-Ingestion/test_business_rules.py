
import pandas as pd
from src.validation.csv_validator import validate_business_rules

file_path = "data/downloaded/transactions_invalid.csv"

df = pd.read_csv(file_path)

result = validate_business_rules(df)

print("Mandatory Field and Business Rule Validation")
print("---------------------------------------------")

print("Total Records:", len(df))
print("Validation Status:", "VALID" if result["is_valid"] else "INVALID")

print("\nValidation Errors:")

for error in result["errors"]:
    print("-", error)

print("\nTotal Errors:", len(result["errors"]))
