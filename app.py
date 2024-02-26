import os
import numpy as np
import tensorflow as tf

import pickle
from PIL import Image
import requests
import streamlit as st
from streamlit_image_comparison import image_comparison
from streamlit_lottie import st_lottie

#page_title and icons
st.set_page_config(layout="wide", page_title="Happy-Sad Classifier", page_icon="😊😔")

#accessing file from github 
def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json()
face = load_lottieurl("https://github.com/nithinganesh1/Image_Classification/raw/main/Animation%20-%201708958036539.json")

#downlad model from github
def load_model():
    trained_model_path = "image_classifier_models.h5"
    if not os.path.isfile(trained_model_path):
        download_url = "https://github.com/nithinganesh1/Image_Classification/raw/main/image_classifier_models/image_classifier_models.h5"
        download_file(download_url, trained_model_path)
    return pickle.load(open(trained_model_path, 'rb'))

trained_model = load_model()

def input_image_setup(img):
    if img is not None:
        # Read the file into bytes
        resize = tf.image.resize(img, (256,256))
        final_data = np.expand_dims(resize/255, 0)

        return final_data
    
    else:
        raise FileNotFoundError("No file uploaded")

    
def predict_img(final_data):
    yhat = trained_model.predict(final_data)
    if yhat > 0.5: 
        prediction = 'Predicted class is Sad'
    else:
        prediction ='Predicted class is Happy'
    return prediction

def main():
    st.header("Happy-Sad People Image Classifier😊😔")

    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with right_column:
            st.write("##")
            st.write("""Use the Happy-Sad People Image Classifier by following these steps: 
             1. Download an image of a person displaying a happy or sad emotion from Google, or use your own image
             2. Click on the 'Upload' button to upload the selected image.
             3. The model will then analyze the image and predict whether the person in the image is happy or sad.
             """)
            
        with left_column:
            st_lottie(face,speed=1,reverse=False,loop=True,quality="low",height=None,width=800,key=None)

        st.write("### Sample Images")
        image_comparison(
                img1="<img src='https://raw.githubusercontent.com/nithinganesh1/Image_Classification/main/sadimg.jpg' alt='Sad Image'>",
                img2="<img src='https://github.com/nithinganesh1/Image_Classification/blob/main/happy%20image.jpg' alt='Happy Image'>",
                label1="sad",
                label2="happy"
                )
    # Get the input data from the user
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = ""   

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
    submit=st.button("Check Emotion")

    if submit:
        final_data = input_image_setup(uploaded_file)
        prediction = predict_img(final_data)
        st.subheader("The emotion is")
        st.write(prediction)