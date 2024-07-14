# OpenWeatherMap ETL data pipeline

This ETL process uses a python script to get current Sapporo weather data.

## Extraction
Data is extracted using requests with the OpenWeatherMap API getting a JSON response.

## Transformation
Data is put into pandas DataFrames, where the temperature figures are converted from degrees Kelvin to degrees Celcius.

## Loading
Data is loaded into a SQLite database for storage, and potential use with a website.
