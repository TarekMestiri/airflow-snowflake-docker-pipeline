from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 9, 25),
    'retries': 0,
}

with DAG(
    dag_id='snowflake_simple_pipeline',
    default_args=default_args,
    description='A simple pipeline to insert dummy data into Snowflake',
    schedule=None, 
    catchup=False,
) as dag:

    insert_data = SQLExecuteQueryOperator(
        task_id='insert_dummy_data',
        conn_id='snowflake_conn',
        sql="""
            INSERT INTO AIRFLOW_DB.PUBLIC.SALES_DATA (ORDER_ID, PRODUCT_NAME, AMOUNT)
            VALUES 
            (101, 'Laptop', 1200.50),
            (102, 'Mouse', 25.00),
            (103, 'Monitor', 350.00);
        """,
    )

    verify_data = SQLExecuteQueryOperator(
        task_id='verify_data_count',
        conn_id='snowflake_conn',
        sql="SELECT COUNT(*) FROM AIRFLOW_DB.PUBLIC.SALES_DATA;",
    )

    insert_data >> verify_data
