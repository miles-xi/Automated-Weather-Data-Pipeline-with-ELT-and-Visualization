'''
this python script is a DAG file that defines the ELT pipeline steps (data workflow)
'''

from airflow import DAG
from airflow.operators.bash import BashOperator  # run bash commands
from datetime import datetime, timedelta

# sets retries if a step fails
default_args = {
    'owner': 'miles',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# define the pipeline
with DAG(
    dag_id='weather_air_quality_pipeline',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval= '*/15 * * * *',  # run every 15 min #'@daily'
    catchup=False,
    tags=['weather', 'elt'],
) as dag:
    
    # bash_command uses /opt/airflow/project/ because Docker maps the elt/ folder to project/ 
    # see docker-compose.yml and the 'volumes' line
    extract = BashOperator(
        task_id='extract_data',  # name that will be used in the Airflow web interface
        bash_command='python /opt/airflow/project/01_extract.py',
    )

    load = BashOperator(
        task_id='load_to_snowflake',
        bash_command='python /opt/airflow/project/02_loadtosnowflake.py',
    )

    transform = BashOperator(
        task_id='run_dbt_transform',
        bash_command='cd /opt/airflow/project/transform-step-container-dbt/weather_transforms && dbt run --profiles-dir ..',
    )

    extract >> load >> transform  # set task order