#installing requests and geopy 
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

#expanding on unique_aiport.ipynb 
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page in range(num_pages):
            page_obj = pdf_reader.pages[page]
            text += page_obj.extract_text()

    return text
  
pdf_file_path = "/Users/megan/Downloads/CIS4400/data/tsa-total-throughput-data-june-11-2023-to-june-17-2023.pdf"
extracted_text = extract_text_from_pdf(pdf_file_path)
print(extracted_text)

#find all the airport codes using regex
airport_codes = re.findall(r'\b[A-Z]{3}\b', extracted_text)

#remove duplicates by converting to a set
unique_airport_codes = list(set(airport_codes))
print(unique_airport_codes)

#function to gather airport latitudes, longitudes 
def get_airport_coordinates(unique_airport_codes):
    geolocator = Nominatim(user_agent="airport_geocoder")

    airport_coordinates = []
    for code in unique_airport_codes:
        location = geolocator.geocode(code)
        if location is not None:
            coordinates = (location.latitude, location.longitude)
            airport_coordinates.append(coordinates)

    return airport_coordinates

#gathering the coordinates 
airport_coordinates = get_airport_coordinates(unique_airport_codes)
print(airport_coordinates)

#getting weather data using the coordinates
def get_weather_data(latitude, longitude):
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,cloudcover&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,uv_index_max,uv_index_clear_sky_max&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&start_date=2023-06-01&end_date=2023-06-30&timezone=EST"
    response = requests.get(weather_url)
    data = response.json()
    return data

#creating the directory path for json files from one PDF 
json_directory = "/Users/megan/Downloads/CIS4400/data/json_directory"

#creating the directory if it doesn't exist
os.makedirs(json_directory, exist_ok=True)

#iterating over the airport coordinates
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
weather_df = pd.DataFrame()

#iterate over each JSON file in the json_directory -- gets weather data for each airport and concatenates
#it into the main weather dataframe. what's missing is the location it correlates with 
for filename in os.listdir(json_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(json_directory, filename)

        #load the JSON file
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        #create a DataFrame for the hourly weather data
        hourly_data = json_data['hourly']
        df = pd.DataFrame(hourly_data)

        #append the DataFrame to the main weather_df
        weather_df = pd.concat([weather_df, df])

#preview the resulting weather DataFrame
weather_df.head()

#save the weather_df DataFrame as a CSV file
weather_csv_path = "/Users/megan/Downloads/CIS4400/data/weather_data.csv"
weather_df.to_csv(weather_csv_path, index=False)
print("weather_df saved as weather_data.csv")

#creating a dataframe with the latitude and longitudes provided. the hourly column is 
#where weather_df comes from 
location_df = pd.DataFrame()

#iterating over the airport coordinates
for latitude, longitude in airport_coordinates:
    location_data = get_weather_data(latitude, longitude)
    
    #convert the weather data to a DataFrame
    df = pd.DataFrame(location_data)
    
     #append the DataFrame to the main weather_df
    location_df = pd.concat([location_df, df])
    
#reset the index of the weather_df
location_df.reset_index(drop=True, inplace=True)

#save the location_df DataFrame as a CSV file
location_csv_path = "/Users/megan/Downloads/cis4400/data/location_data.csv"
location_df.to_csv(location_csv_path, index=False)
print("location_df saved as location_data.csv")

#preview the resulting weather DataFrame
location_df.head()
