# Student Performance ETL Pipeline

A small, reproducible ETL pipeline built with Python, pandas, and SQLite.

The project takes intentionally messy student-performance data, cleans and validates it, and loads the prepared data into CSV and SQLite formats for future analysis or machine learning.

## Project Objective

The goal is to demonstrate how raw data can be transformed into reliable, reusable data through an Extract, Transform, Validate, and Load pipeline.

## Pipeline

```text
Raw CSV data
    ↓
Extract
    ↓
Transform and clean
    ↓
Validate
    ↓
Load into CSV and SQLite
```

## Technologies

- Python
- pandas
- SQLite
- SQL
- Git and GitHub

## What the Pipeline Does

### Extract

Reads raw student-performance data from a CSV file using pandas.

### Transform

The transformation stage:

- Removes duplicate records
- Converts numeric text into numeric values
- Converts invalid numeric values into missing values
- Detects attendance values outside the valid range
- Fills missing numeric feature values using the median
- Replaces missing program values with `UNAVAILABLE`
- Removes records without a valid target score
- Converts program categories into numerical one-hot encoded columns

### Validate

The validation stage checks that:

- Student IDs are unique
- No missing values remain
- Attendance values are between 0 and 100
- Scores are between 0 and 100

The pipeline raises an error if any validation rule fails.

### Load

The cleaned data is saved to:

```text
data/processed/cleaned_student_performance.csv
```

It is also loaded into a SQLite database:

```text
data/processed/student_performance.db
```

The database contains a table named:

```text
student_performance
```

## Project Structure

```text
ETL/
├── data/
│   ├── raw/
│   │   └── student_performance.csv
│   └── processed/
│       ├── cleaned_student_performance.csv
│       └── student_performance.db
├── src/
│   ├── etl_pipeline.py
│   └── query_database.py
├── .gitignore
├── my_environment/
├── requirements.txt
└── README.md
```

The virtual environment and generated processed files are excluded from Git using `.gitignore`.

## Setup

Create and activate a Python virtual environment:

```bash
python3 -m venv my_environment
source my_environment/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the ETL Pipeline

```bash
python src/etl_pipeline.py
```

The pipeline will:

1. Read the raw CSV file
2. Transform the data
3. Validate the cleaned data
4. Save a cleaned CSV file
5. Create a SQLite database

Expected output includes:

```text
Validation passed
Saved cleaned data to data/processed/cleaned_student_performance.csv
Saved SQLite database to data/processed/student_performance.db
```

## Verify the Database

Run:

```bash
python src/query_database.py
```

This queries the SQLite database and confirms that the cleaned records were successfully loaded.

## Important Design Decisions

### Median imputation

Missing numeric feature values are filled using the median because the median is less affected by extreme values than the average.

### Target handling

`exam_score` is the target value. Records without a valid exam score are removed instead of filling in an invented target value.

### One-hot encoding

The `program` category is converted into separate numerical columns. This avoids creating a false ranking between programs.

### Validation before loading

The data is validated before it is saved. This prevents invalid or incomplete data from being loaded into the final outputs.

## Current Limitations

- The dataset is small and created for learning purposes.
- The project does not currently train or evaluate a machine-learning model.
- The pipeline currently uses median values calculated from the available dataset.
- The project does not yet include visual analytics or a dashboard.

## Future Improvements

- Add more realistic data sources
- Add exploratory data analysis and visualizations
- Add SQL summary queries
- Add automated tests
- Add a data-quality report
- Add a machine-learning model
- Add a dashboard using Streamlit

## Resume Description

> Built a Python/pandas ETL pipeline to extract, clean, validate, and load student-performance data into CSV and SQLite formats; handled duplicates, invalid values, missing data, numerical conversion, categorical encoding, and data-quality validation.
