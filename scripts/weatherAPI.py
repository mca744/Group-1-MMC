pip install requests

#importing requests for API 
import requests

#sample latitude parameter - Flushing, NY
lat_param = "40.77"  #insert "latitude" 

#sample longitude parameter - Flushing, NY
long_param = "-73.82" #insert "longitude"

#utilizing API Url's 
base_url ="https://archive-api.open-meteo.com/v1/archive?"

#start date january 01, 2023 to june 01, 2023
base_url2 = "&start_date=2023-01-01&end_date=2023-06-01&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,rain,cloudcover,windspeed_10m,windspeed_100m,winddirection_10m,winddirection_100m&models=best_match&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&min=2023-01-01&max=2023-06-01"
url = base_url + "latitude=" + lat_param + "&longitude=" + long_param + base_url2

#print sample response 
print(response)

#print url
print(url)

#turns response into .json
response = requests.get(url).json()
