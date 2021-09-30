# -*- coding: utf-8 -*-

"""# Exploring the first dataset"""
import pandas as pd
from prophet import Prophet

"""# Spatial Data"""

#read  file 
df2 = pd.read_csv('santander.csv', delimiter=';',decimal=',')

df2.head()

#drop unmamed columns
df2 =df2.drop(columns=['Unnamed: 0'])

#drop rows with nan values
df2 = df2.dropna(subset=['time','latitude','longitude', 'id', 'value'])

#transform time column into datetime
df2['time']= pd.to_datetime(df2['time'])

df2.dtypes

#create second data frame to perform spatial functions
df3_single_locality = df2

#drop all the duplicated entries regarding Latitute, Longitude and the sensor ID
df3_single_locality = df3_single_locality.drop_duplicates(subset=['latitude','longitude','id'])

#define second dataframe as a geodataframe
#import geopandas

#gdf = geopandas.GeoDataFrame(
#    df3_single_locality, geometry=geopandas.points_from_xy(df3_single_locality.longitude, df3_single_locality.latitude))

'''
#Needs a .mapbox_token file to create an interactive plot over the map
import plotly.express as px
px.set_mapbox_access_token(open(".mapbox_token").read())

fig = px.scatter_mapbox(gdf, lat=gdf.geometry.y, lon=gdf.geometry.x, hover_name="id", size_max=15, zoom=10)
fig.show()
'''

'''#Define street names with Latitude and Longitude for each different sensor'''
from geopy.geocoders import Nominatim
# initialize Nominatim API 
geolocator = Nominatim(user_agent="geoapiUrban4Cast")

df3_single_locality.id = df3_single_locality.id.astype(int)
print(df3_single_locality.dtypes)

df3_single_locality = df3_single_locality.drop_duplicates('id', keep=False)

print(df3_single_locality.head())

all_sensors = df3_single_locality['id'].unique()
len(all_sensors)

dict_location = {}

for index, row in df3_single_locality.iterrows():
      # Latitude & Longitude input
      Latitude = row['latitude']
      Longitude = row['longitude']

      location = geolocator.reverse(Latitude+","+Longitude)
      #print(location)

      address = location.raw['address']
      #print(address)

      road = address.get('road', '')
      #print('Sensor: ' + str(row['id']) + ' Road : ', road)
      dict_location[row['id']] = road
 
dict_location.values()

"""# Add information of streets name to the dataframe"""
df2.id = df2.id.astype(int)
df2.value = df2.value.astype(float)
df2.value = df2.value.astype(int)
df2.dtypes

df2['street'] = df2.id.apply(lambda x: dict_location.get(x,' '))

#here we define the street name we are searching
xx = df2[df2['street'] == 'Calle de Hernán Cortés']

xx = xx.rename(columns={"value": "y", "time":"ds"})

"""# Prophet"""

m = Prophet()
m.fit(xx)

future = m.make_future_dataframe(periods=10, freq="10min")
print(future.tail())

forecast = m.predict(future)
print(forecast[['ds','trend', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

fig1 = m.plot(forecast)
fig1.savefig("forecast_bystreet.png")

fig2 = m.plot_components(forecast)
fig2.savefig("components_bystreet.png")

from prophet.diagnostics import cross_validation, performance_metrics
df_cv = cross_validation(m, horizon='2 days')
df_p = performance_metrics(df_cv)
df_p.head(5)


'''
m2 = Prophet(changepoint_prior_scale=0.01).fit(df)
future2 = m2.make_future_dataframe(periods=100, freq='H')
fcst = m2.predict(future2)
fig = m2.plot(fcst)

fig = m2.plot_components(fcst)

from prophet.plot import plot_plotly, plot_components_plotly

plot_plotly(m, forecast)

plot_components_plotly(m, forecast)
'''
