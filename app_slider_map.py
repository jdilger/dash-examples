import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
import plotly.graph_objects as go
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv',
                   dtype={"fips": str}).sort_values(by='date',ascending=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash()
# test add fig
selected_datet = 74
datest = df['date'].unique()
datest = datest[selected_datet]
filtered_df = df[df.date == datest]

figt = go.Figure(go.Choroplethmapbox(geojson=counties, locations=filtered_df.fips, z=filtered_df.cases,
                                    colorscale="Inferno", zmin=0, zmax=2000,
                                    marker_opacity=0.95, marker_line_width=0,))#colorbar={'dtick':'log_10(5)'}
figt.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129}, margin={"r":0,"t":0,"l":0,"b":0})

# end test fig 
app.layout = html.Div([
    dcc.Graph(id='graph-with-slider', figure=figt),
    dcc.Slider(
        id='year-slider',
        min=0,
        max=10,
        value=1,
        marks={0:{'label':'day 1'},
                5:{'label':'day 5'},
                7:{'label':'day7'},
                10:{'label':'day10'}},#{str(date): str(date) for date in df['date'].unique()},
        step=None
    ),
    dcc.Graph(figure=figt)
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])


def update_map(selected_date):
    dates = df['date'].unique()
    dates = dates[selected_date]
    filtered_df = df[df.date == dates]
    print(filtered_df)

    fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=filtered_df.fips, z=filtered_df.cases,
                                        colorscale="Inferno", zmin=0, zmax=2000,
                                        marker_opacity=0.95, marker_line_width=0,))#colorbar={'dtick':'log_10(5)'}
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # print(fig)
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)