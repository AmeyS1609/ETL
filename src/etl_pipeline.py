import pandas as pd
from pathlib import Path

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

    invalid_attendance = ~transformed["attendance_pct"].between(0, 100) # ~ means not/negation
    transformed.loc[
        invalid_attendance,
        "attendance_pct"
    ] = pd.NA
    transformed["program"]= transformed["program"].fillna("UNAVAILABLE").str.strip()
    transformed=transformed.dropna(subset=["exam_score"])

    numeric_feature_column = ["study_hours",
                "attendance_pct",
                "prior_score"]

    for column in numeric_feature_column:
            median_value= transformed[column].median()
            transformed[column] = transformed[column].fillna(median_value)

    program_dummies = pd.get_dummies(
                     transformed["program"],
                     prefix="program",
                     dtype=int
    )
    
    transformed = pd.concat(
        [
            transformed.drop(columns=["program"]),
            program_dummies
        ],
        axis=1
    )
    

    return transformed

def validate_data(data):
    if data["student_id"].duplicated().any():
        raise ValueError("Student IDs are not unique")

    if data.isna().any().any():
        raise ValueError("Missing values remain")

    if not data["attendance_pct"].between(0, 100).all():
        raise ValueError("Attendance is outside the valid range")

    score_columns = [
        "prior_score",
        "exam_score"
    ]

    for column in score_columns:
        if not data[column].between(0, 100).all():
            raise ValueError(f"{column} is outside the valid range")

    return True


raw_data = extract_data("data/raw/student_performance.csv")
cleaned_data=transform(raw_data)

raw_data = extract_data("data/raw/student_performance.csv")
cleaned_data = transform(raw_data)

validate_data(cleaned_data)
print("Validation passed")