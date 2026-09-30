import random
from datetime import datetime
from airflow import DAG
from airflow.providers.common.sql.operators.sql import (
    SQLExecuteQueryOperator, SQLCheckOperator,
)
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

def load_random_rows():
    products = {"Laptop": 1200, "Mouse": 25, "Monitor": 350, "Keyboard": 80}
    rows = []
    for _ in range(5):
        name = random.choice(list(products))
        rows.append((random.randint(1000, 9999), name, products[name]))
    SnowflakeHook(snowflake_conn_id="snowflake_conn").insert_rows(
        table="AIRFLOW_DB.PUBLIC.SALES_DATA",
        rows=rows,
        target_fields=["ORDER_ID", "PRODUCT_NAME", "AMOUNT"],
    )

with DAG(
    dag_id="snowflake_simple_pipeline",
    start_date=datetime(2026, 9, 25),
    schedule="@daily",
    catchup=False,
) as dag:

    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="snowflake_conn",
        sql="""
            CREATE TABLE IF NOT EXISTS AIRFLOW_DB.PUBLIC.SALES_DATA (
                ORDER_ID NUMBER, PRODUCT_NAME STRING, AMOUNT NUMBER(10,2)
            );
        """,
    )

    insert_data = PythonOperator(
        task_id="insert_random_data", python_callable=load_random_rows
    )

    build_summary = SQLExecuteQueryOperator(
        task_id="build_summary",
        conn_id="snowflake_conn",
        sql="""
            CREATE OR REPLACE TABLE AIRFLOW_DB.PUBLIC.SALES_SUMMARY AS
            SELECT PRODUCT_NAME, COUNT(*) AS ORDERS, SUM(AMOUNT) AS TOTAL
            FROM AIRFLOW_DB.PUBLIC.SALES_DATA
            GROUP BY PRODUCT_NAME;
        """,
    )

    check_data = SQLCheckOperator(
        task_id="check_no_bad_rows",
        conn_id="snowflake_conn",
        sql="""
            SELECT COUNT(*) > 0 AND MIN(AMOUNT) >= 0
            FROM AIRFLOW_DB.PUBLIC.SALES_DATA;
        """,
    )

    create_table >> insert_data >> build_summary >> check_data