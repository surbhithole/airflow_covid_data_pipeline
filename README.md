## Goal of the project

The 3,142 counties of the United States span a diverse range of social, economic, health, and weather conditions. County-level data on covid related cases, deaths, usage of mask, college shutdown and weather data can help us understand if the weather and mask use plays an important role in covid spread.

My goal here is to help data scientists analyze covid data accros United States of America based on weather conditionsa and mask usage.

## Data Sources
1) [NY Times Covid Data](https://github.com/nytimes/covid-19-data) 
2) [Kaggle Notebook](https://www.kaggle.com/kerneler/starter-enriched-nytimes-covid19-u-s-69697254-e?select=us_county_pop_and_shps.csv)
3) [NOAA Global Surface Summary of the Day](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00516)

## Data collection and Cleaning:

I used the following datasets for my data pipeline:
1) County Data
2) Mask_use_by_county data
3) College Data
4) County Location Data
5) US weather data
6) Weather stations Data

I collected the weather data for US only. Removed the stations where Latitude and Longitude values were not present.
Using the KNN algorithm, I calculated the nearest counties for each weather station in US.

## Data Model:

![alt text](https://github.com/surbhithole/airflow_covid_data_pipeline/blob/main/covid_data_model.png)

## Steps to create the data model

1) Stage all the data from the folder to redshift.
2) Combine counties data with counties_location data to get the county_center_latitude and county_center_longitude.
3) Get the subset of weather data for US country and combine it with stations data to get the weather stations information.
4) Using KNN find nearest counties to each weather station data using the latitude and longitude information for counties and stations data.
5) Combine college data with county data based on state and county name and get the ipeds_id of the colleges in all the respective counties.

## Run the pipeline

1) [Download Airflow](https://arpitrana.medium.com/install-airflow-on-macos-guide-fc66399b2a9e)
2) [Create a cluster in Redshift](https://docs.aws.amazon.com/redshift/latest/dg/tutorial-loading-data-launch-cluster.html)
4) Modify publicly accesible settings in the newly created cluster
3) Create the [tables](https://github.com/surbhithole/airflow_covid_data_pipeline/blob/main/create_tables.sql) for the pipeline
4) Create connections in Airflow for AWS and Redshift for data transfer.
5) Stage all the data from S3 to Redshift.
6) Run covid_data_dag.py
7) Verify that the data is present in all the respective tables in Redshift.

## What can be done differently?

I used Airflow for this project because what makes Airflow so useful is its ability to handle complex relationships between tasks. You can easily construct tasks that fan-in and fan-out. Tasks are ideally independent pieces that don’t rely on information from another task. Hence, We can create a dag in such a way that the pipeline is created in a most efficient and performant way by clubbing the dependent tasks together.

The data update cycle is typically chosen on two criteria. One is the reporting cycle, the other is the availabilty of new data to be fed into the system. For my project, The covid data is restricted to the number of infections currently present and the year in which it happened considering it is a pandemic disease we are dealing with. Hence I collected the weather just for the year in which Covid related health issues were found. 

IF THIS DATA NEEDED  TO BE CONSIDERED FOR FOLLOWING SCALING FACTORS:

1) If the data was increased by 100x:
   I would have used Spark with Airflow since Apache spark is known for processing large amount of data fast (with in-memory computation), scales easily with additional worker nodes, with ability to digest different data formats (e.g. SAS, Parquet, CSV), and integrate nicely with cloud storage like S3 and warehouse like Redshift.
   
2) If the data populates a dashboard that must be updated on a daily basis by 7am every day:
   I would create a schedule in Airflow which populates the exactly at the time that it is required.
   
3) The database needed to be accessed by 100+ people
   We can consider hosting our solution in production scale data warehouse in the cloud, with larger capacity to serve more users, and workload management to ensure equitable usage of resources across users.

