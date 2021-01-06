from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, SchemaOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'udacity',
    'start_date': datetime.now(),
    'depends_on_past' : False,
    'email_on_failure' : False,
    'email_on_retry'  : False,
    'retries' : 2,
    'retry_delay' : timedelta(minutes = 3),
    'catchup' : False,
}

dag = DAG(
    'covid_data_pipeline_dag',
    default_args = default_args,
    description = "ETL of covid data.",
    schedule_interval = '0 * * * *'
)

start_operator = DummyOperator(task_id = 'Begin_Data_Transfer', dag = dag)

stage_counties_to_redshift = StageToRedshiftOperator(
    task_id = "stage_counties_data",
    dag = dag,
    table = "counties",
    redshift_conn_id = "redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="mycoviddatapipelineproject",
    s3_key="data/us_county_data"
)

stage_mask_use_to_redshift = StageToRedshiftOperator(
    task_id = "stage_mask_data",
    dag = dag,
    table = "mask_use",
    redshift_conn_id = "redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="mycoviddatapipelineproject",
    s3_key="data/mask_use_data"
)

stage_county_location_data_to_redshift = StageToRedshiftOperator(
    task_id = "stage_county_location_data",
    dag = dag,
    table = "county_location_details",
    redshift_conn_id = "redshift",
    aws_credentials_id = "aws_credentials",
    s3_bucket = "mycoviddatapipelineproject",
    s3_key="data/county_location_data"
)

stage_weather_data_to_redshift = StageToRedshiftOperator(
    task_id = "stage_weather_data",
    dag = dag,
    table = "weather_data_us",
    redshift_conn_id = "redshift",
    aws_credentials_id = "aws_credentials",
    s3_bucket = "mycoviddatapipelineproject",
    s3_key = "data/2020_weather_data"
)

stage_weather_stations_data_to_redshift = StageToRedshiftOperator(
    task_id = "stage_stations_data",
    dag = dag,
    table = "stations_table",
    redshift_conn_id = "redshift",
    aws_credentials_id = "aws_credentials",
    s3_bucket = "mycoviddatapipelineproject",
    s3_key = "data/weather_stations"
)

stage_counties_closest_to_stations = StageToRedshiftOperator(
    task_id = "stage_counties_closest_to_stations_data",
    dag = dag,
    table = "counties_close_to_stations",
    redshift_conn_id = "redshift",
    aws_credentials_id = "aws_credentials",
    s3_bucket = "mycoviddatapipelineproject",
    s3_key = "data/counties_to_weather_stations_data"
)


stage_college_data_to_redshift = StageToRedshiftOperator(
    task_id = "stage_college_data_to_redshift",
    dag = dag,
    table = "college_data_by_us_county",
    redshift_conn_id = "redshift",
    aws_credentials_id = "aws_credentials",
    s3_bucket = "mycoviddatapipelineproject",
    s3_key = "data/college_data"
) 

update_weather_data = SchemaOperator(
    task_id='Update_weather_data',
    dag=dag,
    table="final_weather_data",
    redshift_conn_id="redshift",
    truncate_table=True,
    insert_table_query = SqlQueries.weather_table_update
)

update_county_data = SchemaOperator(
    task_id='Update_county_data',
    dag=dag,
    table="final_county_data",
    redshift_conn_id="redshift",
    truncate_table=True,
    insert_table_query = SqlQueries.county_table_update
)

update_fact_table = SchemaOperator(
    task_id = 'update_fact_table',
    dag=dag,
    table="counties_weather_covid_data",
    redshift_conn_id="redshift",
    truncate_table=True,
    insert_table_query = SqlQueries.county_weather_covid_data
)


data_validation_check = DataQualityOperator(
    task_id='Run_data_quality_checks_covid_data',
    dag=dag,
    list_of_tables = ["counties_weather_covid_data", "final_county_data", "final_weather_data", "mask_use", "college_data_by_us_county"],
    redshift_conn_id = "redshift"
)


end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> stage_mask_use_to_redshift
start_operator >> [stage_counties_to_redshift, stage_county_location_data_to_redshift, stage_counties_closest_to_stations]
start_operator >> stage_college_data_to_redshift
start_operator >> [stage_weather_data_to_redshift, stage_weather_stations_data_to_redshift]

[stage_counties_to_redshift, stage_county_location_data_to_redshift, stage_counties_closest_to_stations] >> update_county_data

[stage_weather_data_to_redshift, stage_weather_stations_data_to_redshift] >> update_weather_data

[update_county_data, update_weather_data, stage_college_data_to_redshift] >> update_fact_table
 
update_fact_table >> data_validation_check

data_validation_check >> end_operator 
