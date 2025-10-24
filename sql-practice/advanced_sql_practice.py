import sqlite3
import pandas as pd

# --- Setup: Create an in-memory database and add data ---

# Create a connection to an in-memory database
con = sqlite3.connect(":memory:")
cur = con.cursor()

# Create an 'employees' table
cur.execute("""
CREATE TABLE employees (
    id INTEGER,
    name TEXT,
    department TEXT,
    salary INTEGER
)
""")

# Insert sample data
sample_data = [
    (1, 'Alice', 'Engineering', 90000),
    (2, 'Bob', 'Engineering', 80000),
    (3, 'Charlie', 'Engineering', 95000),
    (4, 'David', 'Sales', 70000),
    (5, 'Eve', 'Sales', 75000),
    (6, 'Frank', 'Marketing', 60000),
    (7, 'Grace', 'Marketing', 80000)
]
cur.executemany("INSERT INTO employees VALUES(?, ?, ?, ?)", sample_data)
con.commit()

# Helper function to print query results neatly
def run_query(query):
    print("--- QUERY ---")
    print(f"{query}\n")
    # Use pandas to read the SQL result into a nice format
    df = pd.read_sql_query(query, con)
    print("--- RESULT ---")
    print(df.to_markdown(index=False))
    print("\n" + "="*30 + "\n")

# --- 1. CTE (Common Table Expression) Example ---
# Goal: Get the names of all employees in the 'Engineering' department.
# A CTE (the 'WITH' clause) creates a temporary table for the query.
query_cte = """
WITH EngineeringEmployees AS (
    SELECT name, salary
    FROM employees
    WHERE department = 'Engineering'
)
SELECT * FROM EngineeringEmployees
WHERE salary > 85000;
"""
run_query(query_cte)


# --- 2. Window Function (RANK) Example ---
# Goal: Rank employees by salary WITHIN each department.
# The 'OVER (PARTITION BY ...)' clause defines the 'window'
query_window_func = """
SELECT
    name,
    department,
    salary,
    RANK() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS dept_salary_rank
FROM employees;
"""
run_query(query_window_func)


# --- 3. Combined CTE and Window Function ---
# Goal: Find the highest-paid employee in EACH department.
query_combined = """
WITH RankedSalaries AS (
    SELECT
        name,
        department,
        salary,
        RANK() OVER (
            PARTITION BY department
            ORDER BY salary DESC
        ) AS dept_rank
    FROM employees
)
SELECT
    name,
    department,
    salary
FROM RankedSalaries
WHERE dept_rank = 1;
"""
run_query(query_combined)


# Close the connection
con.close()