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

#create an empty DataFrame
weather_df = pd.DataFrame()

#iterating over the airport coordinates
for latitude, longitude in airport_coordinates:
    weather_data = get_weather_data(latitude, longitude)
    
    #convert the weather data to a DataFrame
    df = pd.DataFrame(weather_data)
    
     #append the DataFrame to the main weather_df
    weather_df = pd.concat([weather_df, df])
    
#reset the index of the weather_df
weather_df.reset_index(drop=True, inplace=True)

#preview the resulting weather DataFrame
weather_df.head()
