# datamap

Use [missingno](https://github.com/ResidentMario/missingno) library to demonstrate (in)completeness of ```mini-kep``` dataset.

Rough prototype:
```
Annual('a') frequency map:
------------------------------------------------------------
GDP_yoy              |    ****************O*************
CPI_rog              |    ****************O*************
EXPORT_GOODS_usd_bln | ************************O
IMPORT_GOODS_usd_bln | *************************
------------------------------------------------------------
                       1999                            2016

O - missing observation
```

# Possible incosistencies

- time series may start on different dates (it's ok)
- time series not downloaded fully - errors in parsing or upload - will have an omission inside
- some monthly parser not invoked and data not loaded 
- some data dislosed with delay and lags by design (eg BRENT)
- daily data can be reported on wierd dates (USDRUR_CB is published next day, eg Saturday for Friday data)
- other errors we do not know yet

# Download data 

For full dataset data download can use [this code - query_all.py](https://github.com/mini-kep/user-charts/blob/master/query_all.py). It is originally used as a load test and runs about 1 min. 

To construct one dataframe based on individual time series for the ame frequency can use `get_df()` 
[from viz.py](https://github.com/mini-kep/user-charts/blob/8f75d15c855b1d59873ee8d3c8e0dcbf9651514e/viz.py#L24-L29).
