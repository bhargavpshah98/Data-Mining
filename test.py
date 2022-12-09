from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import numpy as np
from sklearn import preprocessing
client = bigquery.Client(project="dataminingproject-364904")
print('fetching zillow data')
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
#df_crimedata=dfquery.to_dataframe(progress_bar_type='tqdm')
print("data")
rows = dfquery.result()  # Waits for query to finish
pdrows=[]
for row in rows:
    print(row)
    pdrows.append([row['State'],row['County'],row['latitude'],row['longitude'],row['location'],row['rent'],row['month']])
df = pd.DataFrame(pdrows, columns=['State', 'County','latitude','longitude','location','rent','month'])
print(df)

edu_encoder = preprocessing.LabelEncoder()
edu_encoder.classes_ = np.load('label_encoder_education.npy')
