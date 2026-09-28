import pandas as pd

def extract_data(path):
    data=pd.read_csv(path)
    return data

def transform(data):
    transformed=data.copy() #so that raw data remains unchanged
    transformed=transformed.drop_duplicates()
    numeric_columns = [
        "study_hours",
        "attendance_pct",
        "prior_score",
        "exam_score"
    ]

    for column in numeric_columns:
        transformed[column]= pd.to_numeric(transformed[column],errors="coerce")

    numeric_feature_column = ["study_hours",
            "attendance_pct",
            "prior_score"]

    for column in numeric_feature_column:
        median_value= transformed[column].median()
        transformed[column] = transformed[column].fillna(median_value)

    invalid_attendance = ~transformed["attendance_pct"].between(0, 100) # ~ means not/negation
    transformed.loc[
    invalid_attendance,
    "attendance_pct"
] = pd.NA
    transformed["program"]= transformed["program"].fillna("UNAVAILABLE").str.strip()
    transformed=transformed.dropna(subset=["exam_score"])

    return transformed

raw_data = extract_data("data/raw/student_performance.csv")
cleaned_data=transform(raw_data)

print(raw_data.head())
print("Raw records:", len(raw_data))
print("Cleaned records:", len(cleaned_data))
print(cleaned_data.head())
print(cleaned_data.dtypes)
print(cleaned_data.isna().sum())