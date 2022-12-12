import numpy as np
import pandas as pd
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from lets_plot import *
from lets_plot.geo_data import *
LetsPlot.setup_html()
import lets_plot
# from plotnine import *
# from plotnine.data import mtcars

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
income_dat["lat"] = income_dat["Lat"]
income_dat["lon"] = income_dat["Lon"]
st.map(income_dat)

# Better Scattering
fill_PiYG= scale_fill_gradient2(name="Mean income", 
                                low="#8e0152",mid="#f7f7f7",high="#276419", 
                                midpoint=mean_US)
color_PiYG = scale_color_gradient2(name="Mean income", 
                                   low="#8e0152",mid="#f7f7f7",high="#276419", 
                                   midpoint=mean_US)

# Define some setting to use on plots later on:
# - Remove axis.
# - Define plot coordinate system and size.
map_settings = (theme(axis="blank", panel_grid="blank") +
                coord_fixed(1.27) +
                ggsize(785, 350))

# Customize the tooltip.
tooltip_scatter=(layer_tooltips()
    .format('Mean', '.2s')
    .line("Mean income|$@Mean"))

st.map(income_dat,10)