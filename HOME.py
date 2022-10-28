#Import Libraries 
import streamlit as st
import numpy as np
import pandas as pd
# from utils.disease import disease_dic
# from utils.fertilizer import fertilizer_dic
import requests
# import config 
import pickle
import io
import torch
from torchvision import transforms
from PIL import Image
import sys
sys.path.append('/home/user/Documents/imgmlreport/inception/models/research/object_detection')
from model import ResNet9   

st.title('Agriculture Zone')

disease_classes = ['Apple___Apple_scab',
                   'Apple___Black_rot',
                   'Apple___Cedar_apple_rust',
                   'Apple___healthy',
                   'Blueberry___healthy',
                   'Cherry_(including_sour)___Powdery_mildew',
                   'Cherry_(including_sour)___healthy',
                   'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                   'Corn_(maize)___Common_rust_',
                   'Corn_(maize)___Northern_Leaf_Blight',
                   'Corn_(maize)___healthy',
                   'Grape___Black_rot',
                   'Grape___Esca_(Black_Measles)',
                   'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                   'Grape___healthy',
                   'Orange___Haunglongbing_(Citrus_greening)',
                   'Peach___Bacterial_spot',
                   'Peach___healthy',
                   'Pepper,_bell___Bacterial_spot',
                   'Pepper,_bell___healthy',
                   'Potato___Early_blight',
                   'Potato___Late_blight',
                   'Potato___healthy',
                   'Raspberry___healthy',
                   'Soybean___healthy',
                   'Squash___Powdery_mildew',
                   'Strawberry___Leaf_scorch',
                   'Strawberry___healthy',
                   'Tomato___Bacterial_spot',
                   'Tomato___Early_blight',
                   'Tomato___Late_blight',
                   'Tomato___Leaf_Mold',
                   'Tomato___Septoria_leaf_spot',
                   'Tomato___Spider_mites Two-spotted_spider_mite',
                   'Tomato___Target_Spot',
                   'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                   'Tomato___Tomato_mosaic_virus',
                   'Tomato___healthy']

disease_model_path = 'models/plant_disease_model.pth'

disease_model = ResNet9(3,len(disease_classes))
disease_model.load_state_dict(torch.load(
    disease_model_path,map_location=torch.device('cpu')))
disease_model.eval()

def switch_page(page_name: str):
    from streamlit import _RerunData, _RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")
    
    page_name = standardize_name(page_name)

    pages = get_pages("streamlit_app.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise _RerunException(
                _RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")
def weather_fetch(city_name):
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid="+api_key+"&q="+city_name
    response = requests.get(complete_url)
    x=response.json()

    if x["cod"] != "404":
        y=x["main"]
        temperature = round((y["temp"] - 273.15),2)
        humidity = y["humidity"]
        return temperature , humidity
    else:
        return  None


def predict_image(img , model= disease_model):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img))
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t,0)

    yb= model(img_u)
    _,preds = torch.max(yb,dim=1)
    prediction = disease_classes[preds[0].item()]
    return prediction



st.header("Get Informed Decisions About Your Farming Strategy.")
st.write("Here Are Some Questions We'll Answer \n 1. What crop to plant here?\n2. What fertilizer to use?\n3. Which disease do your crop have?\n4. How to cure the disease?")

st.subheader("Choose your Service: ")
col1, col2, col3 = st.columns([1,1,1])
page_name =''
with col1:
    temp1 = st.button('Crop')
    st.write("Recommendation about the type of crops to be cultivated which is best suited for the respective conditions")
    if temp1: 
        page_name = 'Crop'
with col2:
    temp2 =st.button("Fertilizer ")
    st.write('Recommendation about the type of fertilizer best suited for the particular soil and the recommended crop')
    if temp2: 
        page_name = 'Fertilizer'
with col3:
    temp3 =st.button("Crop Disease")
    st.write('Predicting the name and causes of crop disease and suggestions to cure it')
    if temp3: 
        page_name = 'crop disease'
if page_name !='':
    switch_page(page_name)