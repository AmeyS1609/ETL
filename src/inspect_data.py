import pandas as pd

data = pd.read_csv("data/raw/student_performance.csv")

print(data.head())
print(f"The data shape is as follows: {data.shape}")
print(data.dtypes)

print(f"# of null cells: {data.isna().sum()}")
print(f"# of duplicated record: {data.duplicated().sum()}")
print(data.columns.tolist())

