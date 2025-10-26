Simple Batch Data Pipeline (API to S3 to dbt)

Project Goal

This project demonstrates a basic, end-to-end batch data pipeline using modern data engineering tools. It extracts data from a public API, loads the raw data into AWS S3, and transforms it using dbt within a Postgres database, orchestrated by Apache Airflow.

This serves as a portfolio project showcasing skills in:

Data Extraction (Python)

Cloud Storage (AWS S3)

Infrastructure as Code (Terraform)

Data Warehousing (Postgres - local simulation)

Data Transformation (dbt)

Workflow Orchestration (Apache Airflow)

Containerization (Docker)

Version Control (Git)

Tech Stack

Orchestrator: Apache Airflow (running via Docker)

Transformation: dbt (Data Build Tool)

Orchestration for dbt: astronomer-cosmos

Data Lake: AWS S3

Data Warehouse: PostgreSQL (running via Docker)

Infrastructure: Terraform

Extraction Scripting: Python (requests, pandas)

Containerization: Docker, Docker Compose

Data Flow (ELT)

[JSONPlaceholder API] -> [Python Script (Extract)] -> [Local JSON File] -> [Airflow Task (Upload)] -> [AWS S3 Bucket (Raw Data)]
                                                                                                        |
                                                                                                        v
                                                                    [Manual/Scripted Load*] -> [Postgres DB (Raw Table)] -> [dbt Models (Transform)] -> [Postgres DB (Analytics Tables)]
                                                                                                        ^
                                                                                                        |
                                                                                            [Airflow TaskGroup (dbt run/test)]


() Note: For simplicity in this initial version, loading data from S3 into the Postgres raw table is simulated or handled manually/via a separate script. In a production scenario, this might involve Airflow S3ToPostgres operators, Snowpipe, Redshift Spectrum, etc.*

Project Structure

simple-data-pipeline/
├── airflow/                 # Airflow setup (docker-compose.yaml, DAGs)
│   ├── dags/
│   │   └── pipeline_dag.py
│   ├── Dockerfile           # Optional: For custom Airflow image needs
│   └── docker-compose.yaml
├── dbt_project/             # Your dbt project files
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   ├── dbt_project.yml
│   └── ... (profiles.yml typically lives outside the project)
├── python_scripts/          # Python scripts called by Airflow
│   └── extract_api_data.py
├── terraform/               # Terraform files for AWS infrastructure
│   ├── main.tf
│   └── variables.tf         # Optional for parameterization
└── README.md                # This file


Setup & Running

Prerequisites:

AWS Account: Configured with Access Key ID and Secret Access Key.

AWS CLI: Installed and configured (aws configure).

Terraform CLI: Installed.

Docker & Docker Compose: Installed and running.

Python 3.9+: For local scripting and virtual environments.

Git: Installed.

Steps:

Clone the Repository:

git clone <your-repo-url>
cd simple-data-pipeline


Set up Python Environment (Optional but Recommended):
Create and activate a virtual environment for local development/testing if needed.

python3 -m venv venv
source venv/bin/activate
# pip install requests pandas boto3 ... (Install necessary libs locally if running scripts outside Docker)


Provision Infrastructure (Terraform):

Navigate to the terraform directory: cd terraform

IMPORTANT: Modify the bucket name in main.tf to make it globally unique.

Initialize Terraform:

terraform init


Review the plan:

terraform plan


Apply the changes to create the S3 bucket:

terraform apply


(Confirm with yes)

Navigate back to the root project directory: cd ..

Set up dbt Profile (for local dbt runs):
Ensure your ~/.dbt/profiles.yml includes a connection profile for your local Postgres instance (the one Airflow will also use, typically managed via Docker). The profile name should match the profile: setting in dbt_project/dbt_project.yml.

Set up Airflow Connection:

Start the local Postgres database (if using a separate docker-compose.yml for it, or ensure the Airflow docker-compose.yml includes it).

Navigate to the airflow directory: cd airflow

Build and start Airflow services:

# Ensure docker-compose.yaml includes postgres, mounts necessary volumes (dags, scripts, dbt_project),
# and installs necessary pip packages (_PIP_ADDITIONAL_REQUIREMENTS) like astronomer-cosmos, boto3, pandas, requests, etc.
docker-compose up -d --build


Wait 1-2 minutes for Airflow to initialize.

Access the Airflow UI (http://localhost:8080, login airflow/airflow).

Go to Admin -> Connections.

Create a Postgres connection (e.g., postgres_default or specifically dbt_postgres_conn if your dbt DAG requires it) pointing to the Postgres service defined in your docker-compose.yaml (Host might be postgres, Login/Password likely airflow/airflow or postgres/postgres depending on compose file).

Create an AWS connection (aws_default) using your AWS credentials (Access Key ID and Secret Access Key). This is needed for the S3 upload task.

Run the Pipeline:

In the Airflow UI, find the DAG (e.g., api_to_s3_to_dbt_pipeline defined in pipeline_dag.py).

Un-pause the DAG using the toggle switch.

Trigger the DAG manually using the play button (▶️).

Monitor the DAG run in the Grid or Graph view.

Destroying Infrastructure

To remove the AWS S3 bucket created by Terraform:

Navigate to the terraform directory: cd terraform

Run the destroy command:

terraform destroy


(Confirm with yes)

Future Improvements

Implement proper loading from S3 to Postgres using an Airflow operator (e.g., S3ToPostgresOperator or a custom Python script using boto3 and psycopg2).

Replace local Postgres with a cloud data warehouse (Snowflake, Redshift, BigQuery) managed by Terraform.

Add more sophisticated error handling and alerting.

Parameterize the API endpoint and S3 bucket names (e.g., using Airflow Variables).

Add data quality checks within the Python extraction script.

Implement schema validation for the API response.
