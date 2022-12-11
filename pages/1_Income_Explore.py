import numpy as np
import pandas as pd
import streamlit as st
import geopandas as gpd
from lets_plot import *
from lets_plot.geo_data import *
LetsPlot.setup_html()
import lets_plot

income_dat = pd.read_csv('./datasets/kaggle_income.csv', encoding='latin-1')
st.write(income_dat.head(3))


