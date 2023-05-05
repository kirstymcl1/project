import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import seaborn as sns
from shapely.geometry import Point

crime = gpd.read_file("data_files/NI_crime_feb_23.csv")
crime.crs = 'epsg:4326'  # sets point crs for crime data
print(crime.head())  # displays first 5 rows of crime data

print(crime['Crime ID'].count())  # counts the number of crimes reported

crime['Crime type'].describe()  # describes dataframe

print(crime.loc[1])  # search row 1 of dataset

print(crime.loc[crime['Crime type'] == 'Anti-social behaviour', 'Crime type'])

ASB_crime = crime.loc[crime['Crime type'] == 'Anti-social behaviour', 'Crime type']

print(ASB_crime)
print(ASB_crime.count())  # counts total number of times ASB crime has been reported


shoplifting_crime = crime.loc[crime['Crime type'] == 'Shoplifting', 'Crime type']
violence_sexual = crime.loc[crime['Crime type'] == 'Violence and sexual offences', 'Crime type']
crimdamage_arson = crime.loc[crime['Crime type'] == 'Criminal damage and arson', 'Crime type']
other_theft = crime.loc[crime['Crime type'] == 'Other theft', 'Crime type']
drugs_crime = crime.loc[crime['Crime type'] == 'Drugs', 'Crime type']
burglary_crime = crime.loc[crime['Crime type'] == 'Burglary', 'Crime type']
other_crime = crime.loc[crime['Crime type'] == 'Other crime', 'Crime type']
vehicle_crime = crime.loc[crime['Crime type'] == 'Vehicle crime', 'Crime type']
poss_weapons = crime.loc[crime['Crime type'] == 'Possessions of weapons', 'Crime type']
public_order = crime.loc[crime['Crime type'] == 'Public order', 'Crime type']
robbery_crime = crime.loc[crime['Crime type'] == 'Robbery', 'Crime type']
bicycle_theft = crime.loc[crime['Crime type'] == 'Bicycle theft', 'Crime type']
theft_from = crime.loc[crime['Crime type'] == 'Theft from the person', 'Crime type']

print(shoplifting_crime.count())
print(violence_sexual.count())
print(crimdamage_arson.count())
print(other_theft.count())
print(drugs_crime.count())
print(burglary_crime.count())
print(other_crime.count())
print(vehicle_crime.count())
print(poss_weapons.count())
print(public_order.count())
print(robbery_crime.count())
print(bicycle_theft.count())
print(theft_from.count())


crimetype = ['Violence_sexual_offences', 'Criminal_damage_arson', 'Other_theft',
             'Shoplifting', 'Drugs', 'Burglary', 'Other_crime', 'Vehicle_crime',
             'Possession_of_weapons', 'Public order', 'Robbery', 'Bicycle_theft',
             'Theft_person', 'Anti-social_behaviour']  # creates list for types of crime

crimecount = [4052, 1310, 1007, 705, 697, 309, 282, 193, 0, 55, 46, 36, 26, 3452]

# creates list for number of reported crimes for each type of crime

plt.bar(crimetype, crimecount)
plt.title('Number of different crimes reported')
plt.xlabel('Crime type')
plt.ylabel('Times reported')
plt.show()

# adapted from https://www.geeksforgeeks.org/bar-plot-in-matplotlib/

# define figure size
bar, ax = plt.subplots(figsize=(16, 9))

# horizontal bar plot
ax.barh(crimetype, crimecount)

# remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)

# remove x, y ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')

# add padding between axes and labels
ax.xaxis.set_tick_params(pad=5)
ax.yaxis.set_tick_params(pad=10)

# show top values
ax.invert_yaxis()

# add Plot Title
ax.set_title('Number of different crimes reported',
             loc='left', )

# Show Plot
plt.show()

df = pd.read_csv('data_files/NI_crime_feb_23.csv')  # loads point data

print(df.head())  # prints initial subset of dataframe

df = df.drop(columns=['Crime ID', 'Falls within', 'LSOA code', 'LSOA name', 'Last outcome category', 'Context'])
# drops colums from dataset

print(df.head())  # shows initial 5 rows of dataset

# add a geometry column from the longitude and latitude coordinates for each crime reported

df['geometry'] = list(zip(df['Longitude'], df['Latitude']))
df['geometry'] = df['geometry'].apply(Point)
print(df)

gdf = gpd.GeoDataFrame(df)  # loads dataframe as gdf
gdf.set_crs("EPSG:4326", inplace=True)  # sets the coordinates reference system
print(gdf)


gdf.to_file('data_files/NIcrimefeb.shp')  # saves gdf as a shapefile

wards = gpd.read_file('data_files/NI_wards.shp')  # load wards shapefile
wards.crs = 'epsg:4326'  # set wards crs
print(wards.head())  # display subset of wards data

print(wards['Ward'].count())  # counts the number of wards in the dataset


wards.plot(figsize=(12, 10))  # plots wards as a map

crimes = gpd.read_file('data_files/NIcrimefeb.shp')  # load crimes shapefile

print(crimes.crs == wards.crs)  # test if crs of both datasets are the same

mapbase = wards.plot(figsize = (12, 10),  # sets figure size
                     color='skyblue',  # sets colour of wards
                     ec='dimgray', linewidth=0.2)  # sets colour and width of wards borders

crimes.plot(ax=mapbase,  # defines axes of map
            marker='.',  # sets the marker shape of the points
            color='indianred',  # sets colour of the points
            markersize=5)  # sets size of the points

join = gpd.sjoin(wards, crimes, how='inner', lsuffix='left', rsuffix='right') #perform the spatial join
join  # show the joined table

crime_stats = join.groupby(['Ward', 'Crime type']).count()  # counts the number of different crimes within each ward
print(crime_stats.head())

drugs_stats = join.groupby('Ward', ['Crime type'] == ['Drugs']).count()  # counts the number of 'Drugs' crime reported in each ward
print(drugs_stats)
print(drugs_stats.loc['Woodvale'])  # prints stats for specific ward

print(join.groupby(['Ward'])['Crime type'].count())  # counts total crime in each ward

join.to_file('data_files/wards_crimes.shp')  # saves join as a shapefile

wards_crimes = gpd.read_file('data_files/wards_crimes.shp')  # loads new shapefile
wards_crimes.crs = 'epsg:4326'  # sets crs
print(wards_crimes.head())  # loads first 5 rows of dataset


polygons = wards  # defines polygons as wards data
polygon_id_field = 'Ward Code'
# points = crimes #
# points.crs = 'epsg:4326'

join = gpd.sjoin(wards, crimes, how='left', predicate='contains')  # defines join for crimes contained within wards
count = join.groupby(polygon_id_field)[polygon_id_field].count()  #  counts number of crime points in polygons
count.name='pointcount'  # sets name for count
polygons = pd.merge(left=polygons, right=count, left_on=polygon_id_field, right_index=True)  # merge the data

fig, ax = plt.subplots(figsize = (20,18))  # sets figure size
polygons.plot(column = 'pointcount', cmap = 'Spectral_r', ax=ax, legend=True, # defines axes and colour ramp of map, this can be changed to suit your visual
              legend_kwds={'label':'Number of crimes reported'})  # defines name of label of the legend
polygons.geometry.boundary.plot(color=None, edgecolor='k',linewidth = 0, ax=ax)  # sets colour and width

#https://towardsdatascience.com/interactive-geographical-maps-with-geopandas-4586a9d7cc10 provides further detail when using interactive maps

crime_count = join.groupby(['Ward'])['Crime type'].count()  # counts number of crimes per ward

ward_count = wards.set_index('Ward').join(crime_count.rename('Crime Count'))  # joins ward and crime_count data
myFig = ward_count.explore(column='Crime Count',  # defines name of legend in the map
                           tooltip=['Ward', 'Population', 'Crime Count'],  # sets what attributes will be shown on hover
                           cmap = 'Spectral_r')  # sets colour ramp of the map

myFig  # display figure

crimes_wards = gpd.read_file('data_files/NI_Wards_Crimes.shp')  # loads new shapefile data
crimes_wards.crs = 'epsg:4326'  # sets crs

crimes_wards.head()  # displays initial 5 rows

crimes_wards.plot.scatter('Point_Coun', 'Population', figsize=(12, 10))  # creates a scatter graph of population and crime rate

sns.lmplot(x = "Point_Coun", y = "Population", data=crimes_wards)  # displays line of best fit to define correlation