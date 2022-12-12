import numpy as np
import pandas as pd
import streamlit as st
import geopandas as gpd
from lets_plot import *
from lets_plot.geo_data import *
LetsPlot.setup_html()
import lets_plot
from plotnine import *
from plotnine.data import mtcars

#Sample Data
income_dat = pd.read_csv('./datasets/kaggle_income.csv', encoding='latin-1')
st.write("DATAFRAME")
st.write(income_dat.head(3))

#Mean Income of US
income_dat = income_dat[~income_dat["State_Name"].isin(["Alaska", "Hawaii", "Puerto Rico"])]
income_dat = income_dat[income_dat["Mean"] > 0]
mean_US = income_dat["Mean"].describe()["mean"]
st.write("MEAN US INCOME")
st.write(mean_US)

#US MAP PLOTTING FOR MEAN INCOME
state_gcoder = geocode_states("US-48")
ggplot() + geom_map(map=state_gcoder) + geom_point(aes("Lon", "Lat", color="Mean"), data=income_dat, size=1)