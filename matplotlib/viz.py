# -*- coding: utf-8 -*-

import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests

from collections import OrderedDict


BASE_URL = 'http://minikep-db.herokuapp.com/api'

FREQUENCIES = OrderedDict([
            ('Annual', 'a'),
            ('Quarterly', 'q'),
            ('Monthly', 'm'),
            ('Daily', 'd')])


def names(freq: str):
    """Get all time series names for a given frequency *freq*."""
    url = f'{BASE_URL}/names/{freq}'
    return requests.get(url).json()


def get_from_api_datapoints(freq, name):
    """Return data for variable *name* and frequency *freq*.
 
    Args:
        freq (str): single letter representing a frequency, ex: 'a'
        name (str): time series name, ex: 'GDP_yoy'

    Returns:
        list of dictionaries like 
        [{'date': '1999-12-31', 'freq': 'a', 'name': 'GDP_yoy', 'value': 106.4},
          ...
          ]
    """
    url = f'{BASE_URL}/datapoints'
    params = dict(freq=freq, name=name, format='json')
    data = requests.get(url, params).json()
    # if parameters are invalid, response is not a jsoned list
    if not isinstance(data, list):
        return []
    return data


def get_time_series(freq, name):
    data = get_from_api_datapoints(freq, name)
    index = pd.to_datetime([d['date'] for d in data])
    values = [d['value'] for d in data]
    return pd.Series(values, index=index, name=name)
    

start = datetime.date(1998, 12, 31)
end = datetime.date(2017, 12, 31)
DEFAULT_TIMERANGE = start, end

# graphics parameters in dicts

SPLINE_GPARAMS = {'timerange': DEFAULT_TIMERANGE,
                  'figsize': (2, 0.6),
                  'style': 'ggplot',
                  'facecolor': 'white',
                  'auto_x': False,
                  'axis_on': False}

INDICATOR_GPARAMS = {'timerange': DEFAULT_TIMERANGE,
                     'figsize': (5, 5),
                     'style': 'bmh',
                     'facecolor': 'white',
                     'auto_x': False,
                     'axis_on': True}

# TODO: we need some nice way to decide at what frequency
#      a time series or a dataframe and return 'a', 'q' or 'm'
#      maybe take first element of the dataframe index add
#      ofsset for month, qtr and year and see which oth them
#      hits the second element in graph


def get_frequency(ts):
    """Returns the frequency of a timeseries or dataframe.
        Args:
            ts: pd.Timeseries
        Returns:
            string
    """
    return str.lower(pd.infer_freq(ts.index))


class GraphBase:
    """Parent class for project charts (Spline, Chart and other)."""

    def __init__(self, ts, params={}):
        """
        Args:
            ts (pd.TimeSeries):
            params (dict): chart formattingstyle parameters
        """
        self.ts = ts
        self.params = params
        # nothing plotted yet
        self.fig = None

    def plot(self):
        plt.style.use(self.params['style'])
        # create figure
        fig = plt.figure(figsize=self.params['figsize'])
        # add 1 subplot and format it
        axes = fig.add_subplot(1, 1, 1, facecolor=self.params['facecolor'])
        axes.set_xlim(self.params['timerange'])
        # draw data at axis
        axes.plot(self.ts)
        # format figure
        if self.params['auto_x']:
            fig.autofmt_xdate()
        if not self.params['axis_on']:
            plt.axis('off')
        self.fig = fig
        return self

    def close(self):
        plt.close()
        self.fig = None


class Spline(GraphBase):
    def __init__(self, ts):
        super().__init__(ts, params=SPLINE_GPARAMS)

class Chart(GraphBase):
    def __init__(self, df, title=None):
        super().__init__(df, params=INDICATOR_GPARAMS)


class ChartStack(GraphBase):
    def __init__(self, df, name=None):
        super().__init__(df, params=INDICATOR_GPARAMS)

    def plot(self):
        plt.style.use(self.params['style'])
        fig = plt.figure(figsize=self.params['figsize'])
        num_plots = len(self.ts.columns)
        for i in range(num_plots):
            ax = fig.add_subplot(num_plots, 1, i + 1)
            ax.plot(df.iloc[:, i])


if __name__ == "__main__":

    ts = get_time_series('q', 'CPI_rog')
    s = Spline(ts)
    c = Chart(ts, 'name2')

    s.plot()
    c.plot()

    varnames = ['RETAIL_SALES_FOOD_bln_rub',
                'RETAIL_SALES_NONFOOD_bln_rub',
                'RETAIL_SALES_bln_rub'
                ]
    df = pd.concat([get_time_series('q', name) for name in varnames], axis=1,
            keys=varnames)
    v = ChartStack(df)
    v.plot()

    # ----------------------------------------
    
    qv = ['GDP_rog'
          'INDPRO_rog',
          'INVESTMENT_rog']

    mv = ['INDPRO_yoy',
          'TRANSPORT_FREIGHT_bln_tkm',
          'CPI_rog',
          'WAGE_REAL_rog',
          'UNEMPL_pct',
          'GOV_SURPLUS_ACCUM_FEDERAL_bln_rub',
          'EXPORT_GOODS_bln_usd',
          'IMPORT_GOODS_bln_usd']

   # ----------------------------------------
    