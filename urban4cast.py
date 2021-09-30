import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as pl
df = pd.read_csv('SmartSantander_processed_dataset.csv', delimiter=';',decimal=',')
print(df.head())
df = df.drop(columns=['Occupancy','OccupiedSpotsNo','OccupiedDuration','AvailabilityDuration','OccupiedDurationPerSpot','OccupiedDurationPercentage','Unnamed: 8','Unnamed: 9'])

import matplotlib.pyplot as plt
fig = plt.figure(facecolor='w', figsize=(20, 6))
plt.plot(df.ds, df.y)

plt.savefig("Currentdata.png")


m = Prophet()
'''
m.add_regressor('OccupiedSpotsNo')
m.add_regressor('OccupiedDuration')
m.add_regressor('AvailabilityDuration')
m.add_regressor('Occupancy')
m.add_regressor('OccupiedDurationPerSpot')
m.add_regressor('OccupiedDurationPercentage')
'''
m.fit(df)

future = m.make_future_dataframe(periods=365)
print(future.tail())

forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

fig1 = m.plot(forecast)
fig1.savefig("forecast.png")


fig2 = m.plot_components(forecast)
fig2.savefig("forecast2.png")

