import streamlit as st
import pickle
import requests
import numpy as np

st.title("Agriculture Zone")
st.sidebar.title("$Agriculture Zone$")
st.header("Find out the most suitable crop to grow in your farm")

crop_recommendation_model = pickle.load(open('RandomForest.pkl', 'rb'))

def weath_cordi(city_name):
    user_api = '7c2bf71bd0d17ce3ab49ab5407df72ab'
    complete_api_link ='http://api.openweathermap.org/geo/1.0/direct?q= ' + city_name + ',' + 'IND' + '&limit='+ '&appid=' + user_api
    api_link = requests.get(complete_api_link)
    x = api_link.json()
    lati = x[0]['lat']
    long = x[0]['lon']
    return lati ,long

def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    lati , long = weath_cordi(city_name)
    user_api = '7c2bf71bd0d17ce3ab49ab5407df72ab'

    # user_api = os.environ['current_weather_data']
    # api_key = config.weather_api_key
    complete_api_link ="https://api.openweathermap.org/data/2.5/weather?lat=" +str(lati) +"&lon="+str(long) +"&appid="+user_api

    # base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    # response = requests.get(complete_api_link)
    api_link = requests.get(complete_api_link)
    x = api_link.json()

    if x["cod"] != "404":
        y = x["main"]
        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None

col1, col2 = st.columns(2)
with st.form('Crop_choice'):
    with col1:
        state = st.selectbox('Select State',
                             ['Andhra Pradesh',
                              'Arunachal Pradesh',
                              'Assam',
                              'Bihar',
                              'Chhattisgarh',
                              'Goa',
                              'Gujarat',
                              'Haryana',
                              'Himachal Pradesh',
                              'Jammu and Kashmir',
                              'Jharkhand',
                              'Karnataka',
                              'Kerala',
                              'Madhya Pradesh',
                              'Maharashtra',
                              'Manipur',
                              'Meghalaya',
                              'Mizoram',
                              'Nagaland',
                              'Odisha',
                              'Punjab',
                              'Rajasthan',
                              'Sikkim',
                              'Tamil Nadu',
                              'Telangana',
                              'Tripura',
                              'Uttar Pradesh',
                              'Uttarakhand',
                              'West Bengal'], index=13
                             )
        nitrogen = st.slider(
            "Please Enter the value of Nitrogen in your soil", value=50)
        phosphorus = slider_val = st.slider(
            "Please Enter The value of Phosphorus in your soil", value=50)
        Pottasium = slider_val = st.slider(
            "Please Enter The value of Pottasium in your soil", value=50)
    with col2:
        city = st.text_input("Enter the City Name", value='Indore')
        phlevel = st.slider("Please Enter the value of ph level in your soil",
                            min_value=0.00, max_value=14.00, value=7.00, step=0.01)
        Rainfall = slider_val = st.slider(
            "Please Enter The value of Rainfall (in mm) in your soil", min_value=0.00, max_value=10.00, value=5.00, step=0.01)
    submitted = st.form_submit_button('Submit')
if submitted:
    st.subheader("In " + state+","+city)
    st.subheader("Minerals in Soil: ")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("Nitrogen : - "+str(nitrogen))
        st.markdown("ph level : - "+str(phlevel))

    with col2:
        st.markdown("Phosphorus : -"+str(phosphorus))
        st.markdown("Rainfall (in mm) : - "+str(Rainfall))
        # st.markdown(city  )
    with col3:
        st.markdown("Pottasium : -"+str(Pottasium))

temperature, humidity = weather_fetch(city)

# st.title(str(temperature)+ "  " + str(humidity))

if weather_fetch(city) != None:
    temperature, humidity = weather_fetch(city)
    data = np.array([[nitrogen,phosphorus, Pottasium, temperature, humidity, phlevel, Rainfall]])
    my_prediction = crop_recommendation_model.predict(data)
    final_prediction = my_prediction[0]
    st.title("You should grow " + final_prediction.upper() +" in your farm" )
    st.sidebar.markdown("$Recommend : " + final_prediction.capitalize() + "$")
else:
    st.title("Results Unable to Fetch , Please Try Againi in Sometime" )
st.sidebar.subheader("About ")
st.sidebar.markdown("Agriculture Zone is a Web Application   \nWhich has Three Purposes   \n 1. Recommend Crop to Farmers based on Place and Soil Minerals ")
st.sidebar.markdown("2. Recommend Fertilizer to farmers according to crop and Soil Minerals")
st.sidebar.markdown("3. Take crop image as an input and describe disease if exist and it's Solutions")
