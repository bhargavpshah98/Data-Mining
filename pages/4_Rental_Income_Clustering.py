import streamlit as st
import pandas as pd
from helpers.dataclient import print_data_classified
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import plotly.figure_factory as ff
import numpy as np

df=print_data_classified()
def header():
    st.write("# Presenting Data and tool")
    st.write("Analyse all locations with jobs which provide highest average pay with least amount of rent")
def best_jobs_state_county():
    st.write("## Best Counties and jobs")
    df_top=df.copy()
    df_top=df_top.loc[df_top['decision']=="BEST"]
    df_top['ratio']=(df_top['rent']*12)/df_top['Annual_Average_Pay']
    df_table=df_top[['County','State','rent','Annual_Average_Pay','Industry','ratio']]
    st.write(df_table)
    df_sample=df_top
    df_sample['State FIPS Code'] = df_sample['state_fips_code'].apply(lambda x: str(x).zfill(2))
    df_sample['County FIPS Code'] = df_sample['county_fips_code'].apply(lambda x: str(x).zfill(3))
    df_sample['FIPS'] =  df_sample['County FIPS Code']
    #df_sample['State FIPS Code'] +
    colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
                "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
                "#08519c","#0b4083","#08306b"]
    endpts = list(np.linspace(0, 0.13, len(colorscale) - 1))
    fips = df_sample['FIPS'].tolist()
    values = df_sample['ratio'].tolist()
    fig = ff.create_choropleth(fips=fips, values=values,binning_endpoints=endpts,colorscale=colorscale,show_state_data=True,show_hover=True, centroid_marker={'opacity': 0},asp=2.9, title='USA Rents by County',legend_title='Rent')
    st.plotly_chart(fig)
def explore_data():
    st.write('## To know if the location is good to move to location based on location and salary')
    df_top=df.copy()
    df_top['ratio']=(df_top['rent']*12)/df_top['Annual_Average_Pay']
    #st.write(df_top)
    # create the dropdown menu for the states
    selected_state = st.selectbox("Select a state:", df_top["State_Name_Full"].unique())

    

    # filter the dataframe to only include the selected state
    filtered_df = df_top.loc[df_top["State_Name_Full"] == selected_state]

    # create the dropdown menu for the counties
    selected_county = st.selectbox("Select a county:", filtered_df["County"].unique())

   

    filtered_df_jobs = filtered_df.loc[filtered_df["County"] == selected_county]
    selected_industry = st.selectbox("Select a Industry:", filtered_df_jobs["Industry"].unique())

    
    # now take the salary
    salary = st.number_input("Enter a salary:", min_value=0,value=24000)
    # display the selected state
    st.write(f"You selected State: {selected_state}")
     # display the selected county
    st.write(f"You selected County: {selected_county}")
    # display the selected county
    st.write(f"You selected Industry: {selected_industry}")
    # display the entered number
    st.write(f"You entered Salary: {salary}")
    # Analysis
    df_table=filtered_df_jobs[['County','State','rent','Annual_Average_Pay','Industry','ratio','decision']]
    
    df_table=df_table.sort_values(by="ratio")
    top=df_table.iloc[0]
    st.write(f"Best Industry for State: {selected_state} and County {selected_county} is {top['Industry']}")
    ratio=((top["rent"]*12)/salary)*100
    if top['Annual_Average_Pay']>salary:
        st.write(f"Your entered salary is way less than average salary in location which is {top['Annual_Average_Pay']} where ideal annual rent to salary ratio is {top['ratio']}")
        st.write(f"The rent in the location will constitute {ratio}% of your salary")
        st.write(f"The usual decision is {top['decision']} if salary is more than {(top['rent']*12*100)*30}")
    else:
        st.write(f"Your Salary is more than average in the location and the decision to choose this location is :{top['decision']} ")
    st.write(f"Some of the best locations for {selected_industry} industry based on rent to salary ratio are")
    df_best=df_top.loc[(df_top['decision']!='BAD') & (df_top['Industry']==selected_industry)]
    df_best_sub=df_best[['County','State','rent','Annual_Average_Pay','Industry','ratio','decision']]
    st.write(df_best_sub)
header()  
best_jobs_state_county()
explore_data()

