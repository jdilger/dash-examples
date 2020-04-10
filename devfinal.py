import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",
                   dtype={"fips": str})

import plotly.graph_objects as go
# init map
tcs = [[0,'rgb(20,11,52)'],[0.3,'rgb(132,32,107)'],[0.85,'rgb(229,92,48)'],[1,'rgb(246,215,70)'] ]
dates = df['date'].unique()
current_date = dates[-1]
current_df = df[df.date == current_date]

fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=current_df.fips, z=current_df.cases,
                                    colorscale=tcs, zmin=0, zmax=2000,
                                    marker_opacity=0.95, marker_line_width=0,))#colorbar={'dtick':'log_10(5)'}
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# available_indicators = df['Indicator Name'].unique()
print(df['cases'])
app.layout = html.Div([
    html.Div([

        html.Div([
        	dcc.Graph(id='covid-map', figure=fig)
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
        	dcc.Graph(id='covid-plot',
	        figure=go.Figure([go.Scatter(x=df['date'], y=df['cases'],mode='markers')]).add_trace(
    							go.Bar(x=df['date'], y=df['deaths']))
	        )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    # dcc.Graph(id='indicator-graphic'),

    # dcc.Slider(
    #     id='year--slider',
    #     min=df['Year'].min(),
    #     max=df['Year'].max(),
    #     value=df['Year'].max(),
    #     marks={str(year): str(year) for year in df['Year'].unique()},
    #     step=None
    # )
])

@app.callback(
    Output('covid-plot', 'figure'),
    [Input('covid-map', 'clickData')])
def updatePlot(county):
	if None:
		return
	click = county['points'][0]['location']
	new_fig = go.Figure([go.Scatter(x=df[df['fips']==click]['date'], y=df[df['fips']==click]['cases'],mode='markers')]).add_trace(
    							go.Bar(x=df[df['fips']==click]['date'], y=df['deaths']))
	return new_fig
if __name__ == '__main__':
    app.run_server(debug=True)