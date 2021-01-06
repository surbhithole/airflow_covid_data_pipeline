The 3,142 counties of the United States span a diverse range of social, economic, health, and weather conditions. County-level data on covid related cases, deaths, usage of mask, college shutdown and weather data can help us understand if the weather and mask use plays an important role in covid spread.

My goal here is to help data scientists analyze covid data accros United States of America.

Data Sources:
1) [NY Times Covid Data](https://github.com/nytimes/covid-19-data) 
2) [Kaggle Notebook](https://www.kaggle.com/kerneler/starter-enriched-nytimes-covid19-u-s-69697254-e?select=us_county_pop_and_shps.csv)
3) [NOAA Global Surface Summary of the Day](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00516)

Data collection and Cleaning:

I used the following datasets for my data pipeline:
1) County Data
2) Mask_use_by_county data
3) College Data
4) County Location Data
5) US weather data
6) Weather stations Data

I collected the weather data for US only. Removed the stations where Latitude and Longitude values were not present.
Using the KNN algorithm, I calculated the nearest counties for each weather station in US. (Python Notebook)

Data Model:



Steps to create the data model:

1) Stage all the data from the folder to redshift.
2) Combine counties data with counties_location data to get the county_center_latitude and county_center_longitude.
3) Get the subset of weather data for US country and combine it with stations data to get the weather stations information.
4) Using KNN find nearest counties to each weather station data using the latitude and longitude information for counties and stations data.
5) Combine college data with county data based on state and county name and get the ipeds_id of the colleges in all the respective counties.
