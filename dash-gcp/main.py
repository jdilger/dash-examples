import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from urllib.request import urlopen
import json
import pandas as pd
import plotly.graph_objects as go
import flask

# Load data
df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",
                   dtype={"fips": str})
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)


# init map
tcs = [[0,'rgb(20,11,52)'],[0.3,'rgb(132,32,107)'],[0.85,'rgb(229,92,48)'],[1,'rgb(246,215,70)'] ]
dates = df['date'].unique()
current_date = dates[-1]
current_df = df[df.date == current_date]
colors = {'bg':'#fcf7fc',
            'txt':'#20293d'}
font_style = {"text-align":"center","font-family":"'Helvetica', serif","font-weight": '400','color':colors['txt'],'line-height': '1.42'}

fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=current_df.fips, z=current_df.cases,
                                    colorscale=tcs, zmin=0, zmax=2000,
                                    marker_opacity=0.95, marker_line_width=0,name='total cases',hoverinfo='z+name'))#colorbar={'dtick':'log_10(5)'}
fig.update_layout(mapbox_style="carto-positron",margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor=colors['bg'],
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})


# test summing for dates
total = df.groupby('date').sum().reset_index()
txt = '''
### COVID-19 Daily Cases By County

A simple map displaying the daily confirmed cases by county for the US. Clicking on a county will
 update the graph to the right showing cumulative cases to date. Data is directly pulled from the [NYT
 Github](https://github.com/nytimes/covid-19-data/). 

Displaying data from: {}
'''.format(current_date)
about = '''
###
About the author: My name is John Dilger, I am a research scientist at [Spatial Informatics Group](https://sig-gis.com)
specializing in remote sensing applications and GIS.
'''

app.layout = html.Div(style={'backgroundColor': colors['bg']},children=[
    html.Div([dcc.Markdown(children=txt)],style=font_style),
    html.Div([

        html.Div([
            dcc.Graph(id='covid-map', figure=fig)
        ],
        style={'width': '60%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='covid-plot',
            figure=go.Figure([go.Scatter(x=total['date'], y=total['cases'],mode='markers')]).update_layout(paper_bgcolor=colors['bg'],title={
            'text': 'Total Cumulative US Cases',
            'y':0.9,
            'x':0.5,
            }))
        ],style={'width': '40%', 'float': 'right', 'display': 'inline-block'})
    ]),

    html.Div([dcc.Markdown(children=about)],style=font_style)

])

@app.callback(
    Output('covid-plot', 'figure'),
    [Input('covid-map', 'clickData')])

def updatePlot(county):
    click = county['points'][0]['location']
    new_fig = go.Figure([go.Scatter(x=df[df['fips']==click]['date'], y=df[df['fips']==click]['cases'],mode='markers')]).update_layout(title={
            'text': 'Total Cases: '+df[df['fips']==click]['county'].iloc[0],
            'y':0.9,
            'x':0.5
            })
    return new_fig

if __name__ == '__main__':
    app.run_server(debug=True,port=8080)