pip install requests

#importing requests for API 
import requests
import pandas as pd 

#sample latitude and longitude parameters
latitudes = ["40.77", "41.23", "39.95"]  # Insert list of multiple latitudes
longitudes = ["-73.82", "-72.97", "-75.16"]  # Insert list of multiple longitudes

#utilizing API Url's
base_url = "https://archive-api.open-meteo.com/v1/archive?"
base_url2 = "&start_date=2023-01-01&end_date=2023-06-01&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,rain,cloudcover,windspeed_10m,windspeed_100m,winddirection_10m,winddirection_100m&models=best_match&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&min=2023-01-01&max=2023-06-01"

#creates an empty DataFrame to store the weather data
weather_data = pd.DataFrame()

for i in range(len(latitudes)):
    # Create the URL for each latitude and longitude combination
    url = base_url + "latitude=" + latitudes[i] + "&longitude=" + longitudes[i] + base_url2
    response = requests.get(url).json()
   
    #converts the response to a df
    df = pd.DataFrame(response)
    
    #appends the df to the weather_data df
    weather_data = weather_data.append(df)

#use this data to append the future tsa_record
#merges the weather_data df with the TSA record on a common key
merged_data = pd.merge(tsa_record, weather_data, on="common_key")

print(merged_data)
    


