# Data
This directory contains pickle files of Pandas data frames of
aggregate consumption data for half-hourly intervals for the past and future as well as individual consumption
data for several households respectively.

The datasets were generated from this [data set](https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households) of SmartMeter Energy Consumption Data in London Households.
Our data exploration can be found in this [Colab](https://colab.research.google.com/drive/1VftNl_ChK36BcLuAtPblGFPqBT_nGEqQ).

*  The 'history' is the data for all timestamps until 2014-01-28 00:00:00.
This is the data that agents have access to for model training.
*  The 'future' is the data for all timestamps from 2014-01-28 00:30:00 to 2014-02-28 00:00:00.
This is the data that agents do not have access to before the demo. As time passes, the can fetch this data
from their `Meter`s (individual consumption) or the `Oracle` (aggregate consumption) via the prediction market.
