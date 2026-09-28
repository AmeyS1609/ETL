import pandas as pd

def extract_data(path):
    data=pd.read_csv(path)
    return data

def transform(data):
    transformed=data.copy() #so that raw data remains uncchanged
    transformed=data.drop_duplicates()
    return transformed

raw_data = extract_data("data/raw/student_performance.csv")

print(raw_data.head())