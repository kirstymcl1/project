import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd 
import cartopy.crs as ccrs
import folium

crime = gpd.read_file()
crime.crs = 'epsg:4326'
crime.head

wards = gpd.read_file()
wards.crs = 'epsg:4326'
wards.head

print(crime.crs == wards.crs)

