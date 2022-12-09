import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

def print_data(project_id="dataminingproject-364904"):
# https://cloud.google.com/resource-manager/docs/creating-managing-projects
    client = bigquery.Client(credentials=credentials,project=project_id)

    #Print your current data
    for dataset in client.list_datasets():
        print(dataset.dataset_id)
    sql = """
            SELECT
                *
            FROM
                `dataminingproject-364904.CrimeCA.crimecadata`
            LIMIT 1000
            """
    dfquery = client.query(sql)
    df_crimedata=dfquery.to_dataframe()
    return df_crimedata
def print_data_zillow_property_price(project_id="dataminingproject-364904"):
# https://cloud.google.com/resource-manager/docs/creating-managing-projects
    client = bigquery.Client(credentials=credentials,project=project_id)

    #Print your current data
    for dataset in client.list_datasets():
        print(dataset.dataset_id)
    sql = """
            SELECT
                *
            FROM
                `dataminingproject-364904.zillow_property_value.ZillowRentProcessed`
            """
    dfquery = client.query(sql)
    df_crimedata=dfquery.to_dataframe()
    return df_crimedata