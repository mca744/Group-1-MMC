pip install requests

#importing requests for API 
import requests

#Sample latitude and longitude parameters
latitudes = ["40.77", "41.23", "39.95"]  # Insert list of multiple latitudes
longitudes = ["-73.82", "-72.97", "-75.16"]  # Insert list of multiple longitudes

# Utilizing API Url's
base_url = "https://archive-api.open-meteo.com/v1/archive?"
base_url2 = "&start_date=2023-01-01&end_date=2023-06-01&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,rain,cloudcover,windspeed_10m,windspeed_100m,winddirection_10m,winddirection_100m&models=best_match&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&min=2023-01-01&max=2023-06-01"

for i in range(len(latitudes)):
    # Create the URL for each latitude and longitude combination
    url = base_url + "latitude=" + latitudes[i] + "&longitude=" + longitudes[i] + base_url2
    response = requests.get(url).json()
    print(response)
    print(url)
