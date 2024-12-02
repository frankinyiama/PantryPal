import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

API_KEY = ''
genai.configure(api_key=API_KEY)


def gen_ai_call(query):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(query)

    return response

def download_button(label, input, file_name, key):
    st.download_button(label, input, file_name=file_name, key=key)

def process_picture(picture):
    query = '''
            Return a Python list that contains all the different ingredients in this picture with each ingrdients starting with a capital letter. If there are no ingredients, return an empty string. DO NOT RETURN ANYTHING ELSE! 
        '''

    image = Image.open(picture)
    model = genai.GenerativeModel('gemini-pro-vision')

    response = model.generate_content([query, image])
    response.resolve()
    response = response.text

    if response == '[]' or '[' not in response:
        response = '[]'

    ingredients = eval(response)

    if not ingredients:
        st.write("Unfortunately, I can't find any ingredients in the picture")
        st.write("If you want to retry, upload a new picture, else, continue")
    else:
        st.write("Here are the ingredients from the picture")
        st.markdown("<ul><li>" + "</li><li>".join(ingredients) + "</li></ul>", unsafe_allow_html=True)

    return ingredients