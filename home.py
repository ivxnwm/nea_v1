import streamlit as st
from custom_libraries.miscellaneous import sidebar


sidebar()

st.title("Home")

st.page_link("question_viewer.py", label="Try out a question", icon="❓")