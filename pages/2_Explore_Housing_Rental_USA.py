import streamlit as st
import pandas as pd
from helpers.dataclient import print_data_zillow_property_price,print_data

df_crime=print_data()
df=print_data_zillow_property_price()

st.set_page_config(
    page_title="Explore Housing Data",
    page_icon="🗺️",
)
st.write("# Crime Data for identifying safety of the location")
st.write("## dataframe")
st.dataframe(df_crime)

st.write("# Property Value across USA over time")
st.write("## dataframe")
st.dataframe(df)

