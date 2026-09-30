import sqlite3
import pandas as pd


database_path = "data/processed/student_performance.db"

with sqlite3.connect(database_path) as connection:
    record_count = pd.read_sql_query(
        """
        SELECT COUNT(*) AS record_count
        FROM student_performance;
        """,
        connection
    )

    sample_data = pd.read_sql_query(
        """
        SELECT student_id, study_hours, attendance_pct, exam_score
        FROM student_performance
        LIMIT 5;
        """,
        connection
    )

print(record_count)
print(sample_data)