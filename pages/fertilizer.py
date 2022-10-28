import streamlit as st
from fertilizer import fertilizer_dic
import pandas as pd

st.title("Agriculture Zone")
st.sidebar.title("$Agriculture Zone$")
st.subheader(
    "Enter Following Detail to choose the fertilizer and take the Informed Decision")

col1, col2 = st.columns(2)
with st.form('Fertilizer_Choice'):
    with col1:
        crop_name = st.selectbox('Select State',
                                 ['rice',
                                  'maize',
                                  'chickpea',
                                  'kidneybeans',
                                  'pigeonpeas',
                                  'mothbeans',
                                  'mungbean',
                                  'blackgram',
                                  'lentil',
                                  'pomegranate',
                                  'banana',
                                  'mango',
                                  'grapes',
                                  'watermelon',
                                  'muskmelon',
                                  'apple',
                                  'orange',
                                  'papaya',
                                  'coconut',
                                  'cotton',
                                  'jute',
                                  'coffee'], index=13)
        nitrogen = st.slider(
            "Please Enter the value of Nitrogen in your soil", value=50)

    with col2:
        phosphorus = slider_val = st.slider(
            "Please Enter The value of Phosphorus in your soil", value=50)
        Pottasium = slider_val = st.slider(
            "Please Enter The value of Pottasium in your soil", value=50)
    submit2 = st.form_submit_button('Submit')


df = pd.read_csv(r"fertilizer.csv")

nr = df[df['Crop'] == crop_name]['N'].iloc[0]
pr = df[df['Crop'] == crop_name]['P'].iloc[0]
kr = df[df['Crop'] == crop_name]['K'].iloc[0]

n = nr-nitrogen
p = pr-phosphorus
k = kr-Pottasium

temp = {abs(n): "N", abs(p): "P", abs(k): "K"}

max_value = temp[max(temp.keys())]
key = ''
if max_value == "N":
    if n < 0:
        key = 'NHigh'
    else:
        key = "Nlow"
elif max_value == "P":
    if p < 0:
        key = 'PHigh'
    else:
        key = "Plow"
else:
    if k < 0:
        key = 'KHigh'
    else:
        key = "Klow"

if submit2:
    st.subheader(str(fertilizer_dic[key]))


st.sidebar.subheader("About ")
st.sidebar.markdown("Agriculture Zone is a Web Application   \nWhich has Three Purposes   \n 1. Recommend Crop to Farmers based on Place and Soil Minerals ")
st.sidebar.markdown("2. Recommend Fertilizer to farmers according to crop and Soil Minerals")
st.sidebar.markdown("3. Take crop image as an input and describe disease if exist and it's Solutions")
