from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Select, RadioButtonGroup
from bokeh.plotting import figure
from bokeh.layouts import column, widgetbox
from collections import OrderedDict
import pandas as pd
import requests


BASE_URL = 'http://minikep-db.herokuapp.com/api'

FREQUENCIES = OrderedDict([
            ('Annual', 'a'),
            ('Quarterly', 'q'),
            ('Monthly', 'm'),
            ('Daily', 'd')])


def get_freq(choice: int):
    """Mapping of an integer index for the active radio button to frequency
       characters for use with the REST API.

    Args:
        choice (integer): integers from 0 to 3 corresponding to each button
    """
    return list(FREQUENCIES.values())[choice]


def get_freq_descriptions():
    """The full word version of each frequency; for use as labels for x-axis
    and the radio buttons.
    """
    return list(FREQUENCIES.keys())


def names(freq):
    """Get all the available indicators for a given frequency."""
    url = f'{BASE_URL}/names/{freq}'
    names = requests.get(url).json()
    return names


def get_from_api_datapoints(freq, name):
    """Datapoints can be generated when a frequency and indicator are
       specified. This is the data which is plotted in the graphs.

    Args:
        freq (char): Single letter representing a frequency
        name (str): An indicator variable name, e.g. GDP_yoy

    Returns:
        Datapoints as a JSON decoded object
    """
    url = f'{BASE_URL}/datapoints'
    params = dict(freq=freq, name=name, format='json')
    data = requests.get(url, params).json()
    if not isinstance(data, list):
         # if parameters are invalid, response is not a jsoned list
         return []
    return data


def get_time_series_dict(freq, name):
    """Process data in column form to feed to plot and callback."""
    data = get_from_api_datapoints(freq, name)
    return dict(x=pd.to_datetime([d['date'] for d in data]),
                y=[d['value'] for d in data])
    

def update_plot(attr, old, new):
    """Bokeh callback function"""
    # step 1. update names selector based on frequency
    selected_freq = get_freq(freq_select.active)
    indicator_select.options = names(selected_freq)
    # step 2. update plot
    selected_indicator = indicator_select.value
    source.data = get_time_series_dict(selected_freq, selected_indicator)
    plot.title.text = f'{selected_indicator}'


def initialize(initial_name, initial_freq):
    """Initialize the plot with default values: 'GDP_yoy' and 'q'.

    Returns:
        A bokeh ColumnDataSource with initial data for the plots, and the
        frequency and indicator selector objects to be used with a callback to
        generate new plots. A bokeh figure object is also returned with a set
        size.
    """
    radio_labels = get_freq_descriptions()
    initial_data = get_time_series_dict(initial_freq, initial_name)
    source = ColumnDataSource(data=initial_data)

    plot = figure(plot_width=400, 
                  plot_height=300, 
                  x_axis_type="datetime")
    plot.line('x', 'y', source=source, color='navy')
    plot.title.text = f'{initial_name}'

    freq_select = RadioButtonGroup(
            labels=radio_labels,
            active=0,
    )
    indicator_select = Select(
        options=names(initial_freq),
        value=initial_name,
        title='indicator'
    )
    return plot, source, freq_select, indicator_select


initial_name = 'GDP_yoy'
initial_freq = 'q'
plot, source, freq_select, indicator_select = \
    initialize(initial_name, initial_freq)

# core bahavior with callbacks        
freq_select.on_change('active', update_plot)
indicator_select.on_change('value', update_plot)

# layout
layout = column(widgetbox(freq_select, indicator_select), plot)
curdoc().add_root(layout)
