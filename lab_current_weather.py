#Retrieves the current weather data from the OpenWeatherMap API

import datetime
import json
import urllib.request

#Function to build the URL for the API request 
def url_builder(lat, lon):
    user_api = '2975d8fae93d5fb86bc1e9f0349a3500' #API key 
    unit = 'metric' #Unit of measurement for temperature
    return 'http://api.openweathermap.org/data/2.5/weather' + \
           '?units=' + unit + \
           '&APPID=' + user_api + \
           '&lat=' + str(lat) +  \
           '&lon=' + str(lon)

#Function to fetch data from the API
def fetch_data(full_api_url):
    url = urllib.request.urlopen(full_api_url) #Opens the URL
    output = url.read().decode('utf-8') #Reads the response and decodes it
    return json.loads(output) #Converts the JSON string to a Python dictionary

#Function to convert the timestamp to a readable format
def time_converter(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d %b %I:%M %p')

# Coordinates for Belfast, UK
lon = -5.93491 #Longtitude value
lat = 54.6032231 #Latitude value

#Fetches the weather data using built URL
json_data = fetch_data( url_builder(lat, lon) )

#Extract relevant data from the JSON response
name = json_data['name'] #City name
temperature = str( json_data['main']['temp'] ) #Current temperature 
timestamp = time_converter( json_data['dt'] ) #Current time 
description = json_data['weather'][0]['description'] #Weather description 
sunset = datetime.datetime.fromtimestamp( json_data['sys']['sunset'] ).strftime('%d %b %I:%M %p') #Sunset time in readable format

#Output
print("Current weather in " + name)
print(timestamp + " : " + temperature +  " : " + description + " : " + sunset)

'''
Modify the code so that:

1. The name of the location is retrieved from the data structure and added to the title message.
name = json_data['name']

2. The forecasted sunset time is displayed.
sunset = str(json_data['sys']['sunset'])
" : " + sunset

'''