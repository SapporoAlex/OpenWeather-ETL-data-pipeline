import requests
import pandas as pd
from sqlalchemy import create_engine

# Define global variables
api_key = 'a76dd3d921db515c5038979c625d7891'
lat = '43.06'
lon = '141.35'
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"


# Function to fetch data from OpenWeatherMap API
def extract():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


# Function to transform data into DataFrames
def transform(data):
    if data:
        # Extract main weather data into DataFrame
        main_df = pd.DataFrame([data['main']])
        main_df['temp'] -= 273.15
        main_df['feels_like'] -= 273.15
        main_df['temp_min'] -= 273.15
        main_df['temp_max'] -= 273.15
        wind_df = pd.DataFrame([data['wind']])
        weather_df = pd.DataFrame(data['weather'])
        return main_df, wind_df, weather_df
    else:
        return None, None, None


# Function to insert main_df into SQL database
def load_into_sql(main_df, table_name, db_uri):
    engine = create_engine(db_uri)
    main_df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    print(f"Data inserted into SQL table '{table_name}'.")


# Main execution flow
if __name__ == "__main__":
    data = extract()
    if data:
        main, wind, weather = transform(data)
        if main is not None and wind is not None and weather is not None:
            # Example database URI (replace with your actual database URI)
            db_uri = 'sqlite:///weather_data.db'
            table_name = 'weather_data'

            # Insert main_df into SQL database
            load_into_sql(main, table_name, db_uri)

            # Save other DataFrames to Excel files
            excel_file1 = "main.xlsx"
            excel_file2 = "wind.xlsx"
            excel_file3 = "weather.xlsx"

            main.to_excel(excel_writer=excel_file1, index=False)
            wind.to_excel(excel_writer=excel_file2, index=False)
            weather.to_excel(excel_writer=excel_file3, index=False)

            print("Data saved to Excel files successfully.")
        else:
            print("Error in transforming data.")
    else:
        print("Failed to fetch data from the API.")
