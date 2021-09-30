# -*- coding: utf-8 -*-

"""# Exploring the first dataset"""

import pandas as pd
from prophet import Prophet

"""# Read data and check elements"""

df = pd.read_csv('SmartSantander_processed_dataset.csv', delimiter=';',decimal=',')

df.head()

"""## Define column DS as datetime"""

df['ds']= pd.to_datetime(df['ds'])

df.dtypes

"""# Prophet"""

#df = df.drop(columns=['y','OccupiedSpotsNo','OccupiedDuration','AvailabilityDuration','OccupiedDurationPerSpot','OccupiedDurationPercentage','Unnamed: 8','Unnamed: 9'])
df = df.drop(columns=['Unnamed: 8','Unnamed: 9'])

import matplotlib.pyplot as plt
fig = plt.figure(facecolor='w', figsize=(20, 6))
plt.plot(df.ds, df.Occupancy)

#currently uses the available spots for prediction
#uncomment the next lines to use occupancy as the predicted value
#df = df.drop(columns=['y'])
#df = df.rename(columns={"Occupancy": "y"})

m = Prophet(changepoint_prior_scale=0.01)
#m.add_regressor('OccupiedSpotsNo')
#m.add_regressor('OccupiedDuration')
#m.add_regressor('AvailabilityDuration')
#m.add_regressor('Occupancy')
#m.add_regressor('OccupiedDurationPerSpot')
#m.add_regressor('OccupiedDurationPercentage')
m.fit(df)

future = m.make_future_dataframe(periods=100, freq="15min")
print(future.tail())

#future['Occupancy'] = future['ds'].apply('Occupancy') 

forecast = m.predict(future)
print(forecast[['ds','trend', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

fig1 = m.plot(forecast)
#fig1.savefig("forecast.png")


fig2 = m.plot_components(forecast)
#fig2.savefig("forecast2.png")

from prophet.diagnostics import cross_validation, performance_metrics
df_cv = cross_validation(m, horizon='1 days')
df_p = performance_metrics(df_cv)
df_p.head(5)

df_cv.head()

'''
import itertools
import numpy as np
import pandas as pd

param_grid = {  
    'changepoint_prior_scale': [0.001, 0.01, 0.1, 0.5],
    'seasonality_prior_scale': [0.01, 0.1, 1.0, 10.0],
}

# Generate all combinations of parameters
all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
rmses = []  # Store the RMSEs for each params here

# Use cross validation to evaluate all parameters
for params in all_params:
    m = Prophet(**params).fit(df)  # Fit model with given params
    df_cv = cross_validation(m, horizon='5 days', parallel="processes")
    df_p = performance_metrics(df_cv, rolling_window=1)
    rmses.append(df_p['rmse'].values[0])

# Find the best parameters
tuning_results = pd.DataFrame(all_params)
tuning_results['rmse'] = rmses
print(tuning_results)
'''

#best_params = all_params[np.argmin(rmses)]
#print(best_params)

from prophet.plot import plot_cross_validation_metric
fig3 = plot_cross_validation_metric(df_cv, metric='mape')

m2 = Prophet(changepoint_prior_scale=0.01).fit(df)
future2 = m2.make_future_dataframe(periods=100, freq="15min")
print(future2.tail())

fcst = m2.predict(future2)
print(fcst[['ds','trend', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

fig = m2.plot(fcst)

fcst
fig = m2.plot_components(fcst)

from prophet.plot import plot_plotly, plot_components_plotly

plot_plotly(m, forecast)

plot_components_plotly(m, forecast)

