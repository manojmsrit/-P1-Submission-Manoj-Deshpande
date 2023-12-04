#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import csv
import pandas
import json 
from math import cos, sqrt, pi
import folium
import webbrowser


R = 6371000 #radius of the Earth in m
csvFilePath = r'food-truck-data.csv'
jsonFilePath = r'food-truck-data.json'
lat_value = input("Enter lattitude value : \n")
long_value = input("Enter longitude value : \n")

"""
Main method in python
"""

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    """
    Convert CSV file data in JSON format for extracting Longitude and Latitude
    """
    csv_to_json(csvFilePath, jsonFilePath)
  

"""
Read CSV file and dump formatted data in JSON format 
"""

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
      
    #read csv file
    with open('food-truck-data.csv', encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
  
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)

"""
Opening JSON file and returns JSON object as a dictionary
"""          

f = open('food-truck-data.json')
data = json.load(f)

# Closing the json file
f.close()


"""
Finding the distance between all the food trucks ased on the given input of latitude and longitude
"""

def distance(lon1, lat1, lon2, lat2):
    lon1 = float(lon1)
    lat1 = float(lat1)
    x = (lon2 - lon1) * cos(0.5*(lat2+lat1))
    y = (lat2 - lat1)
    return (2*pi*R/360) * sqrt( x*x + y*y )


"""
Sorting the food trucks based on the distance to the input of latitude and longitude
"""
food_truck_list = sorted(data, key= lambda d: distance(d["Longitude"], d["Latitude"], float(long_value),  float(lat_value)))


"""
Loading map using folium with default cooridnates and setting up the zoom in and zoom out restrictions
"""

map_obj =folium.Map(location=[37.76008693198698, -122.41880648110114],zoom_start=11,min_zoom=8,max_zoom=14)
#folium.Marker(location=[lat_value, long_value],popup="Input location of the user",tooltip='Input location of the user').add_to(map_obj)


"""
Identification of unique food trucks based on the shortest distance.
Iterating through the list and for every new unique food truck, adding it to the interactive map
Interactive map is updated with food truck name and other details
As per the requirement, once five food truck are found near to the input latitude and longitude values map will be displayed.
"""
unique = []
count = 0
for j in food_truck_list:
    if j['Applicant'] not in unique:
        folium.Marker(location=[j['Latitude'], j['Longitude']],popup=j['Applicant'],tooltip='Click here to see food truck name').add_to(map_obj)
        count += 1
        unique.append(j['Applicant'])
    else:
        continue
    
    if count == 5:
        #folium.Marker(location=[float(lat_value), float(long_value)],popup="Input location of the user",tooltip='Input location of the user').add_to(map_obj)
        break

map_obj.save("food_truck.html")
url = 'food_truck.html'
webbrowser.open(url, new=2)  # open in new tab


if __name__ == '__main__':
    main()
