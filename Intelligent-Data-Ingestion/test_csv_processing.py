from src.validation.csv_validator import inspect_csv

file_path = "data/downloaded/transactions.csv"

result = inspect_csv(file_path)

print("CSV Processing Results")
print("----------------------")
print("Total Rows:", result["rows"])
print("Total Columns:", result["column_count"])
print("Column Names:", result["columns"])

print("\nData Types:")
for column, dtype in result["data_types"].items():
    print(column, ":", dtype)

print("\nMissing Values:")
for column, count in result["missing_values"].items():
    print(column, ":", count)

print("\nSample Records:")
print(result["dataframe"].head())
