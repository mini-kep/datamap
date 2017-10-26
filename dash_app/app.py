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


# NOT TODO: may be a class Data with 
# - Data.names() 
# - data.time_series(freq, name) 

# NOT TODO: frequencies can  be impoereted from db API
def frequencies():
    return [
        {'label': 'Annual', 'value': 'a'},
        {'label': 'Quarterly', 'value': 'q'},
        {'label': 'Monthly', 'value': 'm'},        
        {'label': 'Daily', 'value': 'd'}
    ]


    
BASE_URL = 'http://minikep-db.herokuapp.com/api'

def get_from_api_names(freq):
    url = f'{BASE_URL}/names/{freq}'
    names = requests.get(url).json()
    return [{'label': name, 'value': name} for name in names]


def get_from_api_datapoints(freq, name):
    url = f'{BASE_URL}/datapoints'
    params = dict(freq=freq, name=name, format='json')
    data = requests.get(url, params).json()
    if not isinstance(data, list):
         # if parameters are invalid, response isn't a jsoned list
         return []
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
    
# app.layout controls HTML layout of dcc components on page
# there are three dcc components 
#  - radio items 
#  - dropdown menu
#  - graph with time series
 
app.layout = html.Div([
    dcc.RadioItems(
        options=frequencies(),
        value='a',
        id='frequency'
    ),
    dcc.Dropdown(id='name1', value="GDP_yoy"),
    dcc.Dropdown(id='name2'),
    dcc.Graph(id='time-series-graph')    
], style={'width': '500'})


# NOT TODO: may have - when page is loaded, some graph already shows by default  
#           eg GDP_yoy + q


# NOT TODO: add second graph
    
@app.callback(output=Output('name1', component_property='options'), 
              inputs=[Input('frequency', component_property='value')])
def update_names1(freq):
    return get_from_api_names(freq)


@app.callback(output=Output('name2', component_property='options'), 
              inputs=[Input('frequency', component_property='value')])
def update_names2(freq):
    return get_from_api_names(freq)


@app.callback(output=Output('time-series-graph', 'figure'),
              inputs=[Input('frequency', component_property='value'), 
                      Input('name1', component_property='value'),
                      #Input('name2', component_property='value'),                      
                      ])    
def update_graph(freq, name1, name2=None):
        data1 = get_from_api_datapoints(freq, name1)
        #data2 = get_from_api_datapoints(freq, name2)
        return {
            'data': [{
                'x': [d['date'] for d in data1],
                'y': [d['value'] for d in data1]
                 },    
#    {
#                'x': [d['date'] for d in data2],
#                'y': [d['value'] for d in data2]
#                 }    
    ],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
}






# NOT TODO: what tests should be designed for this code?

# NOT TODO: can deploy to heroku?

# NOT TODO: add second dropdown menu and secdond variable to graph?

# NOT TODO: newer versions
# - sections of variables ('GDP Components', 'Prices'...) 
# - download this data as....
# - human varname description in Russian/English
# - more info about variables as text
# - link to github <https://github.com/mini-kep/intro>

if __name__ == '__main__':
    app.run_server(debug=True)    
    
    
    
    
# EP: parts of dash code seem work in progress
# > help(app)    

#    class Dash(builtins.object)
# |  Methods defined here:
# |  
# |  __init__(self, name=None, server=None, static_folder=None, url_base_pathname='/', **kwargs)
# |      Initialize self.  See help(type(self)) for accurate signature.
# |  
# |  callback(self, output, inputs=[], state=[], events=[])
# |      # TODO - Update nomenclature.
# |      # "Parents" and "Children" should refer to the DOM tree
# |      # and not the dependency tree.
# |      # The dependency tree should use the nomenclature
# |      # "observer" and "controller".
# |      # "observers" listen for changes from their "controllers". For example,
# |      # if a graph depends on a dropdown, the graph is the "observer" and the
# |      # dropdown is a "controller". In this case the graph's "dependency" is
# |      # the dropdown.
# |      # TODO - Check this map for recursive or other ill-defined non-tree
# |      # relationships
