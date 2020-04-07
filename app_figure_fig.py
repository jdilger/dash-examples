from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",
                   dtype={"fips": str})

import plotly.graph_objects as go
from dash.dependencies import Input, Output
# new = df#.groupby(by=['fips','date'])['cases','deaths'].sum().cumsum().reset_index()
# new = new.sort_values(by='date',ascending=True)
# # print(new.iloc[3])
# # new = new.reset_index()
# # test for callback
# #df = new
# selected_date = 74
# dates = new['date'].unique()
# dates = dates[selected_date]
# filtered_df = new[new.date == dates]
# print(dates)
# print(filtered_df)
# # filtered_df = filtered_df[filtered_df['fips']=='06075']

# fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=filtered_df.fips, z=filtered_df.cases,
#                                     colorscale="Inferno", zmin=0, zmax=2000,
#                                     marker_opacity=0.95, marker_line_width=0,))#colorbar={'dtick':'log_10(5)'}
# fig.update_layout(mapbox_style="carto-positron",
#                   mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# # fig.show()
# fig.add_trace( ... )
# fig.update_layout( ... )

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
    id='year-slider',
    min=0,
    max=70,
    value=1,
    marks={0:{'label':'day 1'},
            5:{'label':'day 5'},
            7:{'label':'day7'},
            10:{'label':'day10'},#{str(date): str(date) for date in df['date'].unique()},
			15:{'label':'day 15'},
            18:{'label':'day 18'},
            20:{'label':'day20'},
            24:{'label':'day 24'},
            27:{'label':'day 27'},
            30:{'label':'day30'},
            45:{'label':'day 45'},
            48:{'label':'day 48'},
            60:{'label':'day60'}},
    step=None
	)
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])

def update_map(selected_date):
    dates = df['date'].unique()
    dates = dates[selected_date]
    filtered_df = df[df.date == dates]
    # print(filtered_df)

    fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=filtered_df.fips, z=filtered_df.cases,
                                        colorscale="Inferno", zmin=0, zmax=2000,
                                        marker_opacity=0.95, marker_line_width=0.1,))#colorbar={'dtick':'log_10(5)'}
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=3,) #mapbox_center = {"lat": 37.0902, "lon": -95.7129})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # print(fig)
    return fig
# app.run_server(debug=True)

if __name__ == '__main__':
    app.run_server(debug=True) 