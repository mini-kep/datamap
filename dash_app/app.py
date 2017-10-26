"""Controls and vizualisation for 'mini-kep' dataset using Dash/Plotly

Scenario:

1. select frequency in radio buttons
  -> frequency selection affects list of indicators
  
2. select indicator by name in drop-down menu 
  -> choosing name affects plot
  
3. plot one line as time series

"""

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import requests


app = dash.Dash()


# NOT TODO: frequencies can  be impoereted from db API
def frequencies():
    return [
        {'label': 'Annual', 'value': 'a'},
        {'label': 'Quarterly', 'value': 'q'},
        {'label': 'Monthly', 'value': 'm'},        
        {'label': 'Daily', 'value': 'd'}
    ]


# NOT TODO: may be a class Data with Data.names() and data.time_series(freq, name) 
    
BASE_URL = 'http://minikep-db.herokuapp.com/api'

def get_from_api_names(freq):
    url = f'{BASE_URL}/names/{freq}'
    names = requests.get(url).json()
    return [{'label': name, 'value': name} for name in names]


def get_from_api_datapoints(freq, name):
    url = f'{BASE_URL}/datapoints'
    params = dict(freq=freq, name=name, format='json')
    data = requests.get(url, params).json()
    return data
#
# NOT TODO: may also supply data pre-formatted as:
#             [{
#                'x': [d['date'] for d in data],
#                'y': [d['value'] for d in data]
#            }]
#    



# NOT TODO: may have additional formatting for html
# - centering
# - sans serif font
# - header
    
app.layout = html.Div([
    dcc.RadioItems(
        options=frequencies(),
        id='frequency'
    ),
    dcc.Dropdown(id='names'),
    dcc.Graph(id='time-series-graph')
], style={'width': '500'})


# NOT TODO: may have - when page is loaded, some graph already shows by default  
#           eg GDP_yoy + q

@app.callback(output=Output('names', component_property='options'), 
              inputs=[Input('frequency', component_property='value')])
def update_names(freq):
    return get_from_api_names(freq)

# NOT TODO: similar behaviour can be done with events?

@app.callback(output=Output('time-series-graph', 'figure'),
              inputs=[Input('frequency', component_property='value'), 
                      Input('names', component_property='value')])
def update_graph(freq, name):
        data =  get_from_api_datapoints(freq, name)
        return {
            'data': [{
                'x': [d['date'] for d in data],
                'y': [d['value'] for d in data]
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }

# NOT TODO: what tests should be designed for this code?

# NOT TODO: can deploy to heroku?

# NOT TODO: add second variable?

# NOT TODO: newer versions
# - sections of variables ('GDP Components', 'Prices'...) 
# - download this data as....
# - human varname description in Russian/English
# - more info about variables as text

if __name__ == '__main__':
    app.run_server(debug=True)    