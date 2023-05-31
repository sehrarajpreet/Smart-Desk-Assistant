import requests, json
from Location import IPLocation #Userfile for location webscraper
import re
import pandas as pd
from iso3166 import countries #lib to convert country name to 2 digit code
from datetime import datetime
import numpy as np
import sys
import settings

class InvalidAPIKeyException(Exception):
    "Raised when the api_key file is corrupted or incorrect."
    pass


#Take api_key from txt file
api_file = open("OWM_api_key.txt","r")
file_read = api_file.read()
read_list = list((re.split(" = |\n",file_read)))
api_file.close()

#Small check to see if API key has right length
if len(read_list[1]) != 32:
	raise InvalidAPIKeyException

#get location data from Location class file
loc_object = IPLocation()
loc_object.get_location()

#convert the country to a 2 digit alpha2 code and add it to the end of the user_location list
loc_object.country_code = countries.get(loc_object.country).alpha2

#Use the alpha2 code and city name to get the location's latitude and longitude

def get_coordinates(city,country):
	api_key = read_list[1]
	base_url = "http://api.openweathermap.org/geo/1.0/direct?q="
	complete_url = base_url + city + "&limit=1&appid=" + api_key 
	response = requests.get(complete_url) 
	y = response.json() 

	#add the lat and long to the user_location list
	loc_object.lat = str(y[0]["lat"])
	loc_object.long = str(y[0]["lon"])

get_coordinates(loc_object.city,loc_object.country)


#Using the API keys to get the forecast weather from openweathermapAPI
def weather_now():
	api_key = read_list[1]
	base_url = "https://api.openweathermap.org/data/2.5/forecast?lat="
	city = loc_object.city 
	complete_url = base_url + loc_object.lat + "&lon=" + loc_object.long + "&units=metric&appid=" + api_key
	response = requests.get(complete_url) 
	settings.forecast_response = response.json() 
	columns = ['time', 'temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'sea_level',
    	'grnd_level', 'humidity', 'temp_kf']
	weather_df = pd.DataFrame(columns = columns)


	hr3_forecast_df = pd.DataFrame(columns = list(settings.forecast_response["list"][0]["main"].keys()))

	for item in settings.forecast_response["list"]:
		
		timestamp = item["dt"]
		data1 = list(item["main"].items())
		data1.insert(0,('time', datetime.fromtimestamp(item["dt"])))
		temp_array = np.array(data1).transpose()
		data2 = pd.DataFrame(temp_array[1:],columns = columns)
		hr3_forecast_df = pd.concat([hr3_forecast_df,data2],axis=0,ignore_index=True)
		
	weather_df = pd.concat([weather_df,hr3_forecast_df],axis=0,ignore_index=True)
	
	return weather_df


#Using the API keys to get the current weather from openweathermapAPI
def weather_now_2():
	api_key = read_list[1]
	base_url = "https://api.openweathermap.org/data/2.5/weather?lat="
	city = loc_object.city 
	complete_url = base_url + loc_object.lat + "&lon=" + loc_object.long + "&units=metric&appid=" + api_key 
	response = requests.get(complete_url) 
	settings.weather_response = response.json() 
