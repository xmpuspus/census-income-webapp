# Primary Packages
import pandas as pd
import numpy as np
import streamlit as st

# Package to Load Model
import joblib

@st.cache
def load_data():
    return pd.read_csv('data/census.csv')

data = load_data()

### Set Title
st.title("Income Level Predictor")
st.write("""From the census income data, we built a machine learning-based classification model 
to predict census income level based on their demographics.""")

# Show data
st.subheader('Census Data')
if st.checkbox('Show Raw Data'):
    st.write(data.head(20))

st.sidebar.title('Parameters')

# Age 
age = st.sidebar.slider('Age', 0, 100, 24)

# Hours
hours = st.sidebar.slider('Hours Per Week', 1, 168, 80)

# Education Level
education_level_values = pd.Series(data['education_level'].unique()).str.strip()
education_level_dummies = pd.get_dummies(education_level_values)

education_level_sample = st.sidebar.selectbox("Education Level", education_level_values.values.tolist())

education_level_sample_dummies = (education_level_dummies.loc[np.where(education_level_values.values == education_level_sample)[0]]
                                  .values.tolist()[0])

# Race
race_values = pd.Series(data['race'].unique()).str.strip()
race_dummies = pd.get_dummies(race_values)

race_sample = st.sidebar.selectbox("Race", race_values.values.tolist())
race_sample_dummies = race_dummies.loc[np.where(race_values.values == race_sample)[0]].values.tolist()[0]


# Gender/Sex
sex_values = pd.Series(data['sex'].unique()).str.strip()
sex_dummies = pd.get_dummies(sex_values)

sex_sample = st.sidebar.selectbox("Gender", sex_values.values.tolist())
sex_sample_dummies = sex_dummies.loc[np.where(sex_values.values == sex_sample)[0]].values.tolist()[0]

# Prediction
st.title("Predicted Income Level")

# Load Model
model = joblib.load('model/census_model.pkl')

# Input
sample_features = [age, hours] + education_level_sample_dummies + sex_sample_dummies + race_sample_dummies

# Make Prediction
prediction = model.predict([sample_features])[0]

# Write out prediction
if prediction == True:
    st.write("Income Level is High (Above 50k$ Annually)")
elif prediction == False:
    st.write("Income Level is Low (below 50k$ Annually)")