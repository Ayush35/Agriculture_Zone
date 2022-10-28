import streamlit as st
import numpy as np
import pandas as pd
import pickle
import torch
import io   
from torchvision import transforms
from PIL import Image
from model import ResNet9
from disease import disease_dic

st.title("Agriculture Zone")
st.sidebar.title("$Agriculture Zone$")

# Loading plant disease classification model
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
disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(
    disease_model_path, map_location=torch.device('cpu')))
disease_model.eval()
def predict_image(img,model=disease_model):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor()
    ])
    # image = Image.open(img_file_buffer)
    # img_array = np.array(image)
    image = Image.open(img) 
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t,0)

    #Prediction Model
    yb = model(img_u)
    _,preds = torch.max(yb,dim=1)
    prediction = disease_classes[preds[0].item()]
    return prediction


st.subheader("Disease Classification") 
img=st.file_uploader("Please Upload the Required Image")

if img is not None:
    prediction = predict_image(img)
    crop = prediction.split("__")
    st.sidebar.write("$Crop : "+crop[0]+"$" )
    tdname = crop[1].split('_')
    dname = ''
    for c in tdname:
        if c != '_':
            dname = dname+ " " + c
    st.sidebar.write("$Disease : " + dname +"$")
    st.markdown(str(disease_dic[prediction]))

st.sidebar.subheader("About ")
st.sidebar.markdown("Agriculture Zone is a Web Application   \nWhich has Three Purposes   \n 1. Recommend Crop to Farmers based on Place and Soil Minerals ")
st.sidebar.markdown("2. Recommend Fertilizer to farmers according to crop and Soil Minerals")
st.sidebar.markdown("3. Take crop image as an input and describe disease if exist and it's Solutions")
