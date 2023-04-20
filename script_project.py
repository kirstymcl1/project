import geopandas as gpd
import pandas as pd
import folium

# load crime point data
crime = gpd.read_file("C:/Users/kirst/Documents/egm722/egm722/project/data_files/NI_crime_feb_23.csv")
crime.crs = 'epsg:4326'  # set point crs
print(crime.head)  # display head of point GeoDataFrame
print(crime['Crime ID'].count())  # count number of crimes reported
print(crime.loc[1])  # should display row for Anti-social behaviour crime reported 'On or near Bridge Street'
# displays the rows in which Anti-social behaviour is recorded as Crime Type. Should be 3452 rows in dataset.
print(crime.loc[crime['Crime type'] == 'Anti-social behaviour'])

# covert csv point data into a shapefile
# import necessary modules

from shapely.geometry import Point

df = pd.read_csv('data_files/NI_crime_feb_23.csv')  # loads point data

print(df.head())

df['geometry'] = list(zip(df['Longitude'], df['Latitude']))
df['geometry'] = df['geometry'].apply(Point)
print(df)
# a geometry column of the longitude and latitude coordinates for each crime reported

gdf = gpd.GeoDataFrame(df)
gdf.set_crs("EPSG:4326", inplace=True)  # sets the coordinates reference system
print(gdf)
gdf.to_file('data_files/NI_crime_feb23.shp')

# you can load this and analyse the point data into a GIS software of your choice, e.g. ArcGIS Pro

# load wards shapefile data
wards = gpd.read_file("C:/Users/kirst/Documents/egm722/egm722/project/data_files/NI_Wards.shp")
wards.crs = 'epsg:4326'  # set wards crs
print(wards.head)  # display head of wards gdf
print(wards['Ward'].count())  # count number of wards within Northern Ireland

print(crime.crs == wards.crs)  # confirm that both gdf are set to the same crs

# load counties shapefile data
counties = gpd.read_file("C:/Users/kirst/Documents/egm722/egm722/project/data_files/Counties.shp")
counties.crs = 'epsg:4326'  # set counties crs
print(counties)  # displays counties gdf - should be 6 rows

print(wards.crs == counties.crs)  # confirms that all gdf are set to the same crs

# create a map for crimes within Northern Ireland

# jupyter only %matplotlib inline

import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import os
from cartopy.feature import ShapelyFeature

plt.ion()  # makes the plotting interactive

# generate handles and create a legend for the map

def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# create a scale bar for the map
def scale_bar(ax, location=(0.92, 0.95)):
    x0, x1, y0, y1 = ax.get_extent()
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    ax.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
    ax.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=ax.projection)
    ax.plot([sbx-10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=ax.projection)

    ax.text(sbx, sby-4500, '20 km', transform=ax.projection, fontsize=8)
    ax.text(sbx-12500, sby-4500, '10 km', transform=ax.projection, fontsize=8)
    ax.text(sbx-24500, sby-4500, '0 km', transform=ax.projection, fontsize=8)

# load outline of Northern Ireland as a base for the map

outline = gpd.read_file(os.path.abspath('data_files/NI_outline.shp'))

myFig = plt.figure(figsize=(10, 10))  # create a figure of size 10x10 inches
myCRS = ccrs.UTM(29)  # UTM zone for Northern Ireland
ax = plt.axes(projection=myCRS)  # creates axes for the figure

# can now begin adding data to the map

outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolour='k', facecolour ='w')
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature)  # adds the features created to the map

# concentrate the map to display area of interest
ax.set_extent([xmin-5000, xmax+5000, ymin-5000, ymax+5000], crs=myCRS)

myFig