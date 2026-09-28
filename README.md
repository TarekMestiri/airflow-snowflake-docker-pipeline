# Dockerized Apache Airflow to Snowflake Data Pipeline

A lightweight, production-ready development template designed to orchestrate data ingestion workflows from a containerized **Apache Airflow 3.x** instance directly into a **Snowflake Cloud Data Platform** target architecture. 

This project bypasses proprietary enterprise CLIs, leveraging standard **Docker Compose** architectures and standard Python SQL provider operators to establish a baseline data lifecycle framework natively inside a Windows environment using PowerShell.

## 🚀 Key Features
* **Full Container Orchestration:** Spins up a complete 8-component Airflow environment (Scheduler, Webserver, Worker, Triggerer, API-Server, DAG Processor, Redis, and Postgres DB metadata layer) via a single command.
* **Snowflake Integration:** Native connectivity utilizing the `apache-airflow-providers-snowflake` package to interact directly with remote cloud target endpoints.
* **Idempotent Ingestion Design:** Built-in modular tasks handling mock transaction streams, destination structures, and downstream record verification checks.
* **Tailored for Windows/PowerShell:** Fully configured filesystem structures, environment variable generation paths, and file-sharing permissions optimized for Docker Desktop for Windows architectures.

---

## 🛠️ Architecture & Workflow Overview
The automated workflow (`snowflake_simple_pipeline`) executes on a custom scheduling grid containing sequential dependencies:

1. **Task 1 (`insert_dummy_data`):** Uses the `SQLExecuteQueryOperator` to initiate a remote secure tunnel into Snowflake and inject operational metadata metrics (Order ID, Product Details, Financial Values).
2. **Task 2 (`verify_data_count`):** Validates the data persistence layer by computing warehouse row inventories post-ingestion.


