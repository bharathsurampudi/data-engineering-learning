import datetime

from airflow.decorators import dag, task

# Define a simple Python function.
# The '@task' decorator turns it into an Airflow task.
@task
def my_python_function():
    """This task just prints a message and the date."""
    print("Hello from Airflow!")
    print(f"Today is {datetime.date.today()}")


# This is the main DAG definition.
# The '@dag' decorator turns the function into a DAG.
@dag(
    dag_id="my_first_dag",
    description="A simple tutorial DAG",
    start_date=datetime.datetime(2025, 10, 24), # Change this to today's date
    schedule="@daily",                         # Run once per day
    catchup=False,                             # Don't run for past dates
    tags=["tutorial"],
)
def my_dag():
    """
    This DAG runs one Python function.
    """
    # Call the Python function to create the task instance
    my_python_function()

# This line is needed to actually create the DAG
my_dag()