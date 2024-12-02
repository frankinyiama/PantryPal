import streamlit as st
from st_pages import Page, show_pages

with open('./main.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title("Wellness App Home Page")
show_pages(
   [
       Page("main.py", "Home", "🏠"),
       Page("page2.py", "Pantry Pal", "🍽️")
   ]
)
