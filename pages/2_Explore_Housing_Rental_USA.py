import streamlit as st
import pandas as pd
from helpers.dataclient import print_data_zillow_property_price,print_data
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import plotly.figure_factory as ff

df=print_data_zillow_property_price()

st.set_page_config(
    page_title="Explore Housing Data",
    page_icon="🗺️",
)

st.write("# Property Value across USA over time")
st.write("## dataframe")
st.dataframe(df)


