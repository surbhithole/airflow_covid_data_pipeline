class SqlQueries:   
    weather_table_update = """
    SELECT
        a.stn as station_id,
        b.state as state,
        a.date as "date",
        a.mo as month,
        a.da as day_of_the_month,
        a.temp as temperature,
        a.min as min_temp,
        a.max as max_temp,
        a.prcp as prcp,
        b.lat as station_lat,
        b.lon as station_lon
        FROM
        weather_data_us a
        INNER JOIN stations_table b ON a.stn = b.usaf
        WHERE b.country = 'US'
        """
    
    county_table_update = """
        SELECT 
        a.fips as county_fips_id,
        a.date_of_the_year,
        a.county,
        a.state,
        a.cases as number_of_cases,
        a.deaths as number_of_deaths,
        b.county_center_lat as county_center_latitude,
        b.county_center_lon as county_center_longitude,
        c.km_to_closest_station
        from counties a JOIN county_location_details b
        ON
        a.fips = b.fips
        JOIN counties_close_to_stations c on a.fips = c.fips  
    """
    
    county_weather_covid_data = """
        SELECT 
        a.fips as county_id,
        a.station_id, 
        b.ipeds_id as college_id
        FROM college_data_by_us_county b JOIN counties_close_to_stations a
        on a.county = b.county and a.state = b.state       
    """
    
    #a.km_to_closest_station,