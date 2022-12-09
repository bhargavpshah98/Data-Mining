from flask import Flask, json,g
from google.oauth2 import service_account
from google.cloud import bigquery
from google.cloud import bigquery_storage
import time



companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)

def print_data_zillow_property_price(project_id="dataminingproject-364904"):
# https://cloud.google.com/resource-manager/docs/creating-managing-projects
    client = bigquery.Client(project=project_id)
    bqstorageclient = bigquery_storage.BigQueryReadClient()

    print('loading zillow')
    sql = """
            SELECT
                *
            FROM
                `dataminingproject-364904.zillow_property_value.ZillowPropertyValue`
            LIMIT 1000
            """
    #dfquery = client.query(sql)
    df = client.query(sql).to_arrow(bqstorage_client=bqstorageclient,progress_bar_type='tqdm').to_pandas()
    #df_crimedata=dfquery.to_dataframe(bqstorage_client=bqstorageclient,progress_bar_type='tqdm')
    return df

@api.before_request
def before_request():
    g.start = time.time()

@api.after_request
def after_request(response):
    diff = time.time() - g.start
    if ((response.response) and
        (200 <= response.status_code < 300) and
        (response.content_type.startswith('text/html'))):
        response.set_data(response.get_data().replace(
            b'__EXECUTION_TIME__', bytes(str(diff), 'utf-8')))
    return response

@api.route('/companies', methods=['GET'])
def get_companies():
  df=print_data_zillow_property_price()
  return json.dumps(len(df))

if __name__ == '__main__':
    api.run()