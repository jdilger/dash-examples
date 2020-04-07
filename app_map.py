from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",
                   dtype={"fips": str})

import plotly.graph_objects as go

new = df#.groupby(by=['fips','date'])['cases','deaths'].sum().cumsum().reset_index()
new = new.sort_values(by='date',ascending=True)
# print(new.iloc[3])
# new = new.reset_index()
# test for callback
#df = new
selected_date = 74
dates = new['date'].unique()
dates = dates[selected_date]
filtered_df = new[new.date == dates]
print(dates)
print(filtered_df)
# filtered_df = filtered_df[filtered_df['fips']=='06075']

fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=filtered_df.fips, z=filtered_df.cases,
                                    colorscale="Inferno", zmin=0, zmax=2000,
                                    marker_opacity=0.95, marker_line_width=0,))#colorbar={'dtick':'log_10(5)'}
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
# github

# s = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",parse_dates=['date'],dtype={"fips": str,'date':str})
# d = s.groupby(lambda x: x.date()).aggregate(lambda x: sum(x) if len(x) >= 40 else np.nan)
# print(s.dtypes)
# print (df.groupby(by=['date','fips','county','state']).sum().groupby(level=[0]).cumsum())
# s['cum_sum'] = s.groupby('date').cases.sum()
# print(s.iloc[74],'groubby')
# s["cum_sum"] = s.groupby(s.date).cumsum()
# print(df['cum_sum'])
tfip = '06075'
t = df.groupby(by=['fips','date'])['cases','deaths'].sum().cumsum().reset_index()
print(t[t['fips']==tfip][0:15],'testing')
og = df.groupby(by=['date','fips','county','state']).sum().groupby(level=[0]).cumsum().reset_index()
print(og[og['fips']==tfip][0:15],'og')
all = df
print(df[df['fips']==tfip][0:73],'untouched')