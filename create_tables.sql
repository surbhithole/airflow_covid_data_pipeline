create table counties_weather_covid_data(
	county_id varchar,
    station_id varchar,
    college_id varchar    
)

create table counties_close_to_stations(
	county varchar,
    state varchar,
    fips varchar,
    km_to_closest_station varchar,
    station_id varchar,
    station_name varchar
)

create table final_county_data(
	fips int,
    "date" date,
    county varchar,
    state varchar,
    number_of_cases int,
    number_of_deaths int,
    county_center_latitude varchar,
    county_center_longitude varchar,
    km_to_closest_station varchar
)

create table final_weather_data(
	station_id varchar,
    state varchar,
    "date" varchar,
    month varchar,
    day_of_the_month varchar,
    temperature varchar,
    min_temp varchar,
    max_temp varchar,
    prcp varchar,
    station_lat varchar,
    station_lon varchar
)

create table county_location_details(
	state varchar,
    county varchar,
    fips int,
    county_pop_2019_est varchar,
    county_center_lat varchar,
    county_center_lon varchar
)

create table mask_use(
  countyfp varchar,
  never varchar,
  rarely varchar,
  sometimes varchar,
  frequently varchar,
  always varchar
)

CREATE TABLE counties (
	date_of_the_year date NOT NULL,
	county varchar(256),
	state varchar(256),
	fips int,
	cases int,
    deaths int
);

create table college_data_by_us_county(
  	"date" varchar not null,
    state varchar(256) not null,
    county varchar(256) not null,
    city varchar(256) not null,
    ipeds_id varchar not null,
    college varchar(256) not null,
    cases varchar
)

create table weather_data_us(
  stn varchar,
  wban varchar,
  "date" varchar,
  "year" varchar,
  mo varchar,
  da varchar,
  temp varchar,
  count_temp varchar,
  dewp varchar,
  count_dewp varchar,
  slp varchar,
  count_slp varchar,
  stp varchar,
  count_stp varchar,
  visib varchar,
  count_visib varchar,
  wdsp varchar,
  count_wdsp varchar,
  mxpsd varchar,
  gust varchar,
  "max" varchar,
  flag_max varchar,
  "min" varchar,
  flag_min varchar,
  prcp varchar,
  flag_prcp varchar,
  sndp varchar,
  fog varchar,
  rain_drizzle varchar,
  snow_ice_pallets varchar,
  hail varchar,
  thunder varchar,
  tornado_funnel_cloud varchar
)

create table stations_table(
	usaf varchar,
    wban varchar,
    name varchar,
    country varchar,
    state varchar,
    call varchar,
    lat varchar,
    lon varchar,
    elev varchar,
    "begin" varchar,
    "end" varchar
)