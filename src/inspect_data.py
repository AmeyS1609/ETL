import pandas as pd

data = pd.read_csv("data/raw/student_performance.csv")

print(data.head())
print(f"The data shape is as follows: {data.shape}")
print(data.dtypes)

