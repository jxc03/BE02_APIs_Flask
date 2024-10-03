import json
import urllib.request

def url_builder(lat, lon):
    user_api = 'b13c69eca47b941b84b44306ea24c081'
    unit = 'metric'
    return 'http://api.openweathermap.org/data/2.5/weather' + \
        '?units=' + unit + \
        '&APPID=' + user_api + \
        '&lat=' + str(lat) + \
        '&lon=' + str(lon)

def fetch_data(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    return json.loads(output)

def get_temperature(lat, lon):
    json_data = fetch_data(url_builder(lat, lon))
    temperature = json_data['main']['temp']
    city_name = json_data['name']
    return temperature, city_name

def get_lat_lon(prompt):
    while True:
        try:
            lat = float(input(f"Enter latitude for {prompt}: "))
            lon = float(input(f"Enter longitude for {prompt}: "))
            return lat, lon
        except ValueError:
            print("Invalid input. Please enter numeric values")


location1 = get_lat_lon("Location 1")
location2 = get_lat_lon("Location 2")

temp1, city1 = get_temperature(*location1)
temp2, city2 = get_temperature(*location2)

if temp1 > temp2:
    hotter_city = city1
    hotter_temp = temp1
    cooler_city = city2
    cooler_temp = temp2
elif temp1 < temp2:
    hotter_city = city2
    hotter_temp = temp2
    cooler_city = city1
    cooler_temp = temp1
else:
    print("Both cities have the same temperature:")
    exit()

print(f"{hotter_city} is hotter than {cooler_city}.")
print(f"{hotter_city}: {hotter_temp}°C, {cooler_city}: {cooler_temp}°C")

'''
Write a Python program compare_temperatures.py:
1. That prompts the user for two latitude and longitude values representing a pair of locations and uses the
OpenWeatherMap API to retrieve the location name and current temperature
for each. The program should output the result in the form (e.g.) “Belfast is
hotter than Berlin”.
'''