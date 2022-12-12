import streamlit as st
import pandas as pd
from helpers.dataclient import print_data_zillow_property_price,print_data
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import plotly.figure_factory as ff
import numpy as np

df=print_data_zillow_property_price()

st.set_page_config(
    page_title="Explore Housing Data",
    page_icon="🗺️",
)

def exploreByCounty():
    st.write("# Show Trend By County")
    form = st.form(key='rent_form')
    min_value = df['rent'].min()
    max_value = df['rent'].max()
    
    state_options = df["State"].unique()
    state_form_input = form.selectbox("Choose State:", state_options)
    rent_in = form.slider('rent:', min_value=min_value, max_value=max_value,step=200.0,value=(min_value,max_value))
    
    sumbit=form.form_submit_button()
    if sumbit: 
        st.write(rent_in)
        st.write(state_form_input)
        df_merged=df.loc[(df['State'] == state_form_input) & (df['rent'] >= rent_in[0]) & (df['rent'] <= rent_in[1])]
        topCountyrentsMax = pd.DataFrame(df_merged[df_merged['month'] == '2022-10-31'].groupby(['County'])['rent'].sum()).reset_index().sort_values(by='rent', ascending=False).reset_index(drop=True).loc[:10,'County'].values
        fig = go.Figure()
        df_counts=[]
        for county in topCountyrentsMax:
            
            info_state = pd.DataFrame(df_merged[df_merged['County'] == county].groupby('month')['rent'].sum()).reset_index().sort_values(by='month')
            df_temp=info_state.copy()
            df_temp['County']=[county for i in range(len(df_temp))]
            df_counts.append(df_temp)
            fig.add_trace(go.Scatter(x=info_state.month, y=info_state.rent, name=county))
        fig.update_layout(title_text='Rent in top 10 Counties with maximum rent in state '+state_form_input, title_x=0.5)
        st.plotly_chart(fig)    

def drawTop10():
    st.write("# Show Top 10 Counties")
    df_merged=df
    topCountyrentsMax = pd.DataFrame(df_merged[df_merged['month'] == '2022-10-31'].groupby(['County'])['rent'].sum()).reset_index().sort_values(by='rent', ascending=False).reset_index(drop=True).loc[:10,'County'].values
    fig = go.Figure()
    df_counts=[]
    for county in topCountyrentsMax:
        info_state = pd.DataFrame(df_merged[df_merged['County'] == county].groupby('month')['rent'].sum()).reset_index().sort_values(by='month')
        df_temp=info_state.copy()
        df_temp['County']=[county for i in range(len(df_temp))]
        df_counts.append(df_temp)
        fig.add_trace(go.Scatter(x=info_state.month, y=info_state.rent, name=county))
    fig.update_layout(title_text='Rent in top 10 Counties with maximum rent', title_x=0.5)
    st.plotly_chart(fig)
def drawBottom10():
    st.write("# Show Top 10 Counties")
    df_merged=df
    topCountyrentsMin = pd.DataFrame(df_merged[df_merged['month'] == '2022-10-31'].groupby(['County'])['rent'].sum()).reset_index().sort_values(by='rent', ascending=True).reset_index(drop=True).loc[:10,'County'].values
    fig = go.Figure()
    df_counts=[]
    for county in topCountyrentsMin:
        info_state = pd.DataFrame(df_merged[df_merged['County'] == county].groupby('month')['rent'].sum()).reset_index().sort_values(by='month')
        df_temp=info_state.copy()
        df_temp['County']=[county for i in range(len(df_temp))]
        df_counts.append(df_temp)
        fig.add_trace(go.Scatter(x=info_state.month, y=info_state.rent, name=county))
    fig.update_layout(title_text='Rent in top 10 Counties with minimum rent', title_x=0.5)
    st.plotly_chart(fig)

def drawChoroPleth():
    st.write("# Chloropleth chart")
    df_sample = df[df['month']=='2022-10-31'].copy()
    df_sample['State FIPS Code'] = df_sample['state_fips_code'].apply(lambda x: str(x).zfill(2))
    df_sample['County FIPS Code'] = df_sample['county_fips_code'].apply(lambda x: str(x).zfill(3))
    df_sample['FIPS'] =  df_sample['County FIPS Code']
    #df_sample['State FIPS Code'] +
    colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
                "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
                "#08519c","#0b4083","#08306b"]
    endpts = list(np.linspace(1, 12, len(colorscale) - 1))
    fips = df_sample['FIPS'].tolist()
    values = df_sample['rent'].tolist()
    fig = ff.create_choropleth(fips=fips, values=values,binning_endpoints=endpts,colorscale=colorscale,show_state_data=False,show_hover=True, centroid_marker={'opacity': 0},asp=2.9, title='USA Rents by County',legend_title='Rent')
    st.plotly_chart(fig)
exploreByCounty()
drawTop10()
drawBottom10()
drawChoroPleth()
#


