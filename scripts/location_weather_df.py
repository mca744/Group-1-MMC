import sys 
!{sys.executable} -m pip install requests geopy

#importing libraries
import requests
from geopy.geocoders import Nominatim
import json
import PyPDF2
import re
import pandas as pd
import os

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in pdf_reader.pages])
    return text

#Providing paths to PDF files
pdf_file_paths = [
    "/Users/megan/Downloads/CIS4400/data/tsa-total-throughput-data-may-28-2023-to-june-3-2023.pdf",
    "/Users/megan/Downloads/CIS4400/data/tsa-total-throughput-data-june-4-2023-to-june-10-2023.pdf",
    "/Users/megan/Downloads/CIS4400/data/tsa-total-throughput-data-june-11-2023-to-june-17-2023.pdf",
    "/Users/megan/Downloads/CIS4400/data/tsa-total-throughput-data-june-18-2023-to-june-24-2023.pdf"
]

#initializing an empty set for airport codes
unique_airport_codes = set()

#iterating over each PDF file
for pdf_file_path in pdf_file_paths:
    extracted_text = extract_text_from_pdf(pdf_file_path)
    airport_codes = re.findall(r'\b[A-Z]{3}\b', extracted_text)
    unique_airport_codes.update(airport_codes)

#convert the set of unique airport codes to a list
unique_airport_codes = list(unique_airport_codes)
print(unique_airport_codes)

#creating a function to get the airport coordinates (lat/longs)
def get_airport_coordinates(unique_airport_codes):
    geolocator = Nominatim(user_agent="airport_geocoder")

    airport_coordinates = []
    for code in unique_airport_codes:
        location = geolocator.geocode(code)
        if location is not None:
            coordinates = (location.latitude, location.longitude)
            airport_coordinates.append(coordinates)

    return airport_coordinates

#providing a list of airport coordinates (lats/longs)
airport_coordinates = get_airport_coordinates(unique_airport_codes)
print(airport_coordinates)

#creating a DataFrame with airport codes and coordinates
location_df = pd.DataFrame(data=airport_coordinates, columns=['Latitude', 'Longitude'], index=unique_airport_codes[:-1])
location_df.reset_index(inplace=True)
location_df.rename(columns={'index': 'AirportCode'}, inplace=True)

#previewing the resulting location DataFrame
print(location_df)

#creating a function to get weather data for each coordinate or a specific time 
def get_weather_data(latitude, longitude):
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,cloudcover&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,uv_index_max,uv_index_clear_sky_max&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&start_date=2023-05-28&end_date=2023-06-24&timezone=EST"
    response = requests.get(weather_url)
    data = response.json()
    return data

#creating the directory path
json_directory = "/Users/megan/Downloads/CIS4400/data/json_directory2"

#creating the directory if it doesn't exist
os.makedirs(json_directory, exist_ok=True)

#iterating over the airport coordinates to eventually combine all weather info into one dataframe
for i, (latitude, longitude) in enumerate(airport_coordinates):
    weather_data = get_weather_data(latitude, longitude)

    #convert the weather data to JSON format
    json_data = json.dumps(weather_data)

    #create a filename for the JSON file
    filename = f"{json_directory}/{airport_codes[i]}_weather.json"

    #write the JSON data to a file
    with open(filename, 'w') as file:
        file.write(json_data)

    print(f"Saved weather data for airport {i+1}")

print("All weather data saved successfully.")

#create an empty DataFrame to store the combined weather data
weather_df2 = pd.DataFrame()

#iterating over each JSON file in the json_directory 
for filename in os.listdir(json_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(json_directory, filename)
        airport_code = filename.split("_")[0]  # extract the airport code from the filename

        #load the JSON file
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        #create a DataFrame for the hourly weather data
        hourly_data = json_data['hourly']
        df = pd.DataFrame(hourly_data)

        # add columns for airport code, latitude, and longitude
        df['AirportCode'] = airport_code
        df['Latitude'] = location_df.loc[location_df['AirportCode'] == airport_code, 'Latitude'].values[0]
        df['Longitude'] = location_df.loc[location_df['AirportCode'] == airport_code, 'Longitude'].values[0]

        #append the DataFrame to the main weather_df
        weather_df2 = pd.concat([weather_df2, df])

#preview the resulting weather DataFrame with all airport codes, airport lat/longs info 
weather_df2.head()

#save the weather_df DataFrame as a CSV file
weather_csv_path = "/Users/megan/Downloads/CIS4400/data/weather_data_final.csv"
weather_df2.to_csv(weather_csv_path, index=False)
print("weather_df2 saved as weather_data.csv")
