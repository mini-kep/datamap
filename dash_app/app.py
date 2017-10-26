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



def frequencies():
    return [
        {'label': 'Annual', 'value': 'a'},
        {'label': 'Quarterly', 'value': 'q'},
        {'label': 'Monthly', 'value': 'm'},
        {'label': 'Weekly', 'value': 'w'},
        {'label': 'Daily', 'value': 'd'}
    ]


BASE_URL = 'http://minikep-db.herokuapp.com/api'

def names(freq):
    url = f'{BASE_URL}/names/{freq}'
    names = requests.get(url).json()
    return [{'label': name, 'value': name} for name in names]


def datapoints(freq, name):
    url = f'{BASE_URL}/datapoints'
    data = requests.get(url, params=dict(
        freq=freq,
        name=name,
        format='json'
    )).json()
    return data


app.layout = html.Div([
    dcc.RadioItems(
        options=frequencies(),
        id='frequency'
    ),
    dcc.Dropdown(id='names'),
    dcc.Graph(id='data-graph')
], style={'width': '500'})


@app.callback(Output('names', 'options'), [Input('frequency', 'value')])
def update_names(freq):
    return names(freq)


@app.callback(Output('data-graph', 'figure'),
            [Input('frequency', 'value'), Input('names', 'value')])
def update_graph(freq, name):
        data = datapoints(freq, name)
        return {
            'data': [{
                'x': [d['date'] for d in data],
                'y': [d['value'] for d in data]
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }


if __name__ == '__main__':
    app.run_server(debug=True)