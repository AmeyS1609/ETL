import pandas as pd
from pathlib import Path
import sqlite3

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

def load_data(data, output_path):
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data.to_csv(
        output_path,
        index=False
    )

def load_to_sqlite(data, database_path):
    database_path = Path(database_path)
    database_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with sqlite3.connect(database_path) as connection:
        data.to_sql(
            "student_performance",
            connection,
            if_exists="replace",
            index=False
        )

raw_data = extract_data("data/raw/student_performance.csv")
cleaned_data=transform(raw_data)

validate_data(cleaned_data)
print("Validation passed")

output_path = "data/processed/cleaned_student_performance.csv"

load_data(cleaned_data, output_path)

print(f"Saved cleaned data to {output_path}")

database_path = "data/processed/student_performance.db"

load_to_sqlite(
    cleaned_data,
    database_path
)

print(f"Saved SQLite database to {database_path}")