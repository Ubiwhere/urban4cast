# -*- coding: utf-8 -*-

"""# Exploring the datasets"""

import pandas as pd
from prophet import Prophet

df = pd.read_csv('trafic_capteurs_2019_W51_20191229_20200101.csv', delimiter=';')

df = df.dropna(subset=['q','k'])

df =df.drop(columns=['dessin'])

df = df.rename(columns={"etat_trafic": "y", "t_1h":"ds"})
df.q = df.q.astype(int)
df.k = df.k.astype(float)
df.etat_barre = df.etat_barre.astype(int)
df = df.sort_values(by='ds')

df['ds']= pd.to_datetime(df['ds'])

m = Prophet()
m.add_regressor('q')
m.add_regressor('k')
m.add_regressor('etat_barre')
m.fit(df)

future = m.make_future_dataframe(periods=10, freq="D")
print(future.tail())

future = future.merge(df, on='ds')
forecast = m.predict(future)
print(forecast[['ds','trend', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

fig1 = m.plot(forecast)
fig1.savefig("forecast_traffic.png")


fig2 = m.plot_components(forecast)
fig2.savefig("components_traffic.png")

from prophet.diagnostics import cross_validation, performance_metrics
df_cv = cross_validation(m, horizon='8 h')
df_p = performance_metrics(df_cv)
df_p.head(5)

xx = df[df['libelle'] == 'Pyrenees']
xx = xx.sort_values(by='ds')
xx

m = Prophet()
m.add_regressor('q')
m.add_regressor('k')
m.add_regressor('etat_barre')
m.fit(xx)

future = m.make_future_dataframe(periods=10, freq="D")
print(future.tail())

future = future.merge(df, on='ds')
forecast = m.predict(future)
print(forecast[['ds','trend', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

fig1 = m.plot(forecast)
fig1.savefig("forecast_traffic_byroad.png")


fig2 = m.plot_components(forecast)
fig2.savefig("components_traffic_byroad.png")
