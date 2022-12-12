import numpy as np
import pandas as pd
from sklearn import preprocessing
import streamlit as st
from helpers.dataclient import print_data_zillow_property_price
import pickle
from sklearn.linear_model import LogisticRegression

form = st.form(key='predict_form')

def fetchEncoder(filename):
    encoder = preprocessing.LabelEncoder()
    encoder.classes_ = np.load(filename,allow_pickle=True)
    return encoder

df=pd.read_csv('./datasets/adult_census_processed.csv')
#st.write(df)
# Get a list of unique values in the "column" column
wc_options = df["workclass"].unique()
edu_options = df["education"].unique()
sex_options = df["sex"].unique()
occ_options = df["occupation"].unique()
race_options = df["race"].unique()
rel_options=df["relationship"].unique()
ms_options=df["marital.status"].unique()


age_input = form.slider('Enter your age:', min_value=10, max_value=80)
# Create a form with a dropdown field
wc_form_input = form.selectbox("Choose Work Class:", wc_options)
# Create a form with a dropdown field
education_form_input = form.selectbox("Choose education:", edu_options)
# Create a form with a dropdown field
sex_form_input = form.selectbox("Choose sex:", sex_options)
# Create a form with a dropdown field
race_form_input = form.selectbox("Choose race:", race_options)
# Create a form with a dropdown field
occ_form_input = form.selectbox("Choose occupation:", occ_options)
# Create a form with a dropdown field
ms_form_input = form.selectbox("Choose Marital status:", ms_options)
# Create a form with a dropdown field
rel_form_input = form.selectbox("Choose relationship :", rel_options)
hrs_per_week = form.slider('Hours Per Week:', min_value=1, max_value=140)

country="United-States"
submit=form.form_submit_button() 


cat_dict={}
cat_dict["workclass"]="./models/predictbasic/label_encoder_workclass.npy"
cat_dict["marital.status"]="./models/predictbasic/label_encoder_marital.status.npy"
cat_dict["occupation"]="./models/predictbasic/label_encoder_occupation.npy"
cat_dict["relationship"]="./models/predictbasic/label_encoder_relationship.npy"
cat_dict["education"]="./models/predictbasic/label_encoder_education.npy"
cat_dict["race"]="./models/predictbasic/label_encoder_race.npy"
cat_dict["sex"]="./models/predictbasic/label_encoder_sex.npy"
cat_dict["native.country"]="./models/predictbasic/label_encoder_native.country.npy"
if submit:
    df_new=pd.DataFrame([[age_input,wc_form_input,education_form_input,ms_form_input,occ_form_input,rel_form_input,race_form_input,sex_form_input,hrs_per_week,country]],columns=['age','workclass','education','marital.status','occupation','relationship','race','sex','hours.per.week','native.country'])
    st.write(df_new)
    df_inf=df_new.copy()
    categorical = ['workclass', 'education', 'marital.status', 'occupation', 'relationship', 'race', 'sex', 'native.country']
    for feature in categorical:
            label = fetchEncoder(cat_dict[feature])
            df_inf[feature] = label.transform(df_inf[feature])
            
    st.write(df_inf)
    
    # Load the logistic regression model from the pickle file
    with open("./models/predictbasic/model.pkl", "rb") as file:
        model = pickle.load(file)
        # Load the logistic regression model from the pickle file
    with open("./models/predictbasic/scaler.pkl", "rb") as file:
        scaler = pickle.load(file)
    X_test = pd.DataFrame(scaler.transform(df_inf), columns = df_inf.columns)
    # Make predictions using the model
    predictions = model.predict(X_test)
    print(predictions)
    st.write('prediction',predictions[0])