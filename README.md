## Setup & Running (Detailed)

**Prerequisites:** Ensure all required tools (AWS CLI, Terraform CLI, Docker, Python, Git) are installed and configured as outlined previously.

**Steps:**

1.  **Clone:** Get the code:
    ```bash
    git clone <your-repo-url>
    cd simple-data-pipeline
    ```

2.  **Infrastructure (Terraform):** Create the S3 bucket.
    * `cd terraform`
    * **CRITICAL:** Edit `main.tf` and change `bucket = "..."` to a **globally unique name**. Use hyphens, lowercase letters, and numbers. Add your initials or random numbers.
    * Run `terraform init` to download the AWS provider.
    * Run `terraform plan` to preview the changes (should show 1 resource to create).
    * Run `terraform apply` and type `yes` to create the bucket.
    * `cd ..`

3.  **dbt Profile:** Configure how dbt connects locally (used by `cosmos` indirectly and for local testing).
    * Locate or create `~/.dbt/profiles.yml` (in your user home directory).
    * Add an entry matching the `profile:` name in `dbt_project/dbt_project.yml`. Ensure `host`, `port`, `user`, `password`, `dbname` point to the **Postgres container** defined in your Airflow `docker-compose.yaml`. The `host` might be `localhost` if accessing from your host machine, but might be the *service name* (e.g., `postgres`) if connecting from another container. Use the correct credentials.
        ```yaml
        # Example for profile named 'my_first_project' connecting to Docker Postgres
        my_first_project:
          target: dev
          outputs:
            dev:
              type: postgres
              host: localhost # Or 'postgres' service name from docker-compose
              port: 5432
              user: airflow # Or postgres user from docker-compose
              password: airflow # Or postgres password from docker-compose
              dbname: airflow # Or postgres db name from docker-compose
              schema: public # Default schema for dbt output initially
              threads: 1
        ```

4.  **Airflow Setup:** Prepare and start Airflow services.
    * `cd airflow`
    * **Review `docker-compose.yaml`:**
        * Confirm a `postgres` service is defined (or linked externally).
        * Verify necessary **volumes** are mounted: `./dags:/opt/airflow/dags`, `../python_scripts:/opt/airflow/scripts`, `../dbt_project:/opt/airflow/dbt_project`.
        * Check `_PIP_ADDITIONAL_REQUIREMENTS` under `x-airflow-common` -> `environment`. It **must** include `--constraint <URL> astronomer-cosmos[dbt-postgres] requests pandas boto3`. Add any other required Python libs here.
    * Run `docker-compose up -d --build`. This builds the image (installing packages) and starts all services (webserver, scheduler, postgres, redis). Wait for completion.
    * **Wait 1-2 minutes** for Airflow components to fully initialize.

5.  **Airflow Connections:** Configure how Airflow tasks connect to external systems.
    * Go to `http://localhost:8080`, log in (`airflow`/`airflow`).
    * Go to **Admin -> Connections -> + Add a new record**.
    * **Create Postgres Connection:**
        * `Conn Id`: `dbt_postgres_conn` (must match `conn_id` in your DAG's `ProfileConfig`)
        * `Conn Type`: `Postgres`
        * `Host`: `postgres` (This is typically the service name defined in `docker-compose.yaml`)
        * `Schema`: `airflow` (Or the Postgres database name defined in `docker-compose.yaml`)
        * `Login`: `airflow` (Or the Postgres user from `docker-compose.yaml`)
        * `Password`: `airflow` (Or the Postgres password from `docker-compose.yaml`)
        * `Port`: `5432`
        * Click **Save**.
    * **Create AWS Connection:**
        * `Conn Id`: `aws_default` (Standard convention used by many AWS operators/hooks)
        * `Conn Type`: `Amazon Web Services`
        * `AWS Access Key ID`: Paste your IAM user's Access Key ID.
        * `AWS Secret Access Key`: Paste your IAM user's Secret Access Key.
        * (Optional) Specify region if needed.
        * Click **Save**.

6.  **Run Pipeline:** Execute the workflow.
    * In the Airflow UI (DAGs view), find your pipeline DAG (e.g., `dbt_orchestration_taskgroup_dag`). It might take a minute to appear after startup.
    * Click the toggle to un-pause it.
    * Click the play button (▶️) to trigger a manual run.
    * Monitor the progress in the Grid or Graph view. Check task logs for details or errors.

## Destroying Infrastructure

When finished, remove the S3 bucket to avoid AWS charges.

1.  `cd terraform`
2.  `terraform destroy` (and confirm with `yes`)
3.  `cd ..`

## Future Improvements

* **Automated S3->Postgres Loading:** Implement this crucial step using Airflow operators or a dedicated Python task.
* **Cloud Data Warehouse:** Migrate from local Postgres to Snowflake/Redshift/BigQuery, managing it with Terraform.
* **Error Handling/Alerting:** Add mechanisms (e.g., Airflow email/Slack alerts) for pipeline failures.
* **Parameterization:** Use Airflow Variables/Connections to make API endpoints, bucket names, etc., configurable without changing code.
* **Enhanced Testing:** Add more dbt tests and potentially data validation in the Python extraction step.
* **Schema Management:** Introduce schema validation (e.g., using Pydantic for API responses) or schema evolution tools.
