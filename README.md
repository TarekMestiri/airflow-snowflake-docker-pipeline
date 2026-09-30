# Dockerized Apache Airflow to Snowflake Data Pipeline

A lightweight development template for orchestrating a small data pipeline from a containerized Apache Airflow 3.x instance into Snowflake.

It uses standard Docker Compose and the official Airflow SQL and Snowflake providers, and it is set up to run on Windows with Docker Desktop and PowerShell.

## 🚀 Key Features

* **Full container orchestration:** starts the whole Airflow stack (API server, scheduler, DAG processor, Celery worker, triggerer) plus Redis and Postgres with a single `docker compose up`.
* **Snowflake integration:** connects through the `apache-airflow-providers-snowflake` package, using both SQL operators and the Snowflake hook.
* **Self-contained pipeline:** creates its own table, loads generated sample data, builds a summary table, and validates the result.
* **Windows-friendly:** file paths, environment variable setup, and permissions are configured for Docker Desktop on Windows.

## 🛠️ Workflow Overview

The DAG `snowflake_simple_pipeline` runs daily with sequential dependencies:

1. **`create_table`**: creates `SALES_DATA` if it does not already exist.
2. **`insert_random_data`**: a Python task that uses `SnowflakeHook` to insert five randomly generated sales rows (order ID, product, amount).
3. **`build_summary`**: rebuilds `SALES_SUMMARY` with the order count and total amount per product.
4. **`check_no_bad_rows`**: a data quality check that fails the run if the table is empty or contains a negative amount.

```
create_table >> insert_random_data >> build_summary >> check_no_bad_rows
```

## ⚙️ Setup

1. Create the Snowflake warehouse, database, schema, and `SALES_DATA` table.
2. Copy your settings into a `.env` file (`AIRFLOW_UID`, `FERNET_KEY`). This file is git-ignored.
3. Start the stack with `docker compose up -d`.
4. In the Airflow UI, create a `snowflake_conn` connection with your account, warehouse, database, and role.
5. Unpause and trigger `snowflake_simple_pipeline` at http://localhost:8080.

> This project is meant for learning and local development. Do not commit credentials, and rotate the Fernet key if it is ever exposed.
