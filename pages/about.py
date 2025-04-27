#
import streamlit as st
from custom_libraries.miscellaneous import sidebar
from streamlit_extras.let_it_rain import rain

#! --- Page ---
sidebar()
st.logo("res/Blueberrevise logo 5.png", size="large")

rain(
    emoji="🫐",
    font_size=72,
    falling_speed=10,
    animation_length=1,
)

st.title("About")
st.write("This is my NEA project for A Level Computer Science!")
