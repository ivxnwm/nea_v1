# This chatbot uses Google Gemini API
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
import PIL.Image as im


def gemini_configuration():
    # Standard gemini configuration
    load_dotenv()
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    system_instructions = ("You are a knowledgeable and helpful maths teacher "
                           "who can explain concepts clearly and concisely. "
                           "When a student asks you something, you identify the point of confusion "
                           "and provide a step-by-step explanation to help them understand the concept. "
                           "You can also provide examples and analogies to help the student grasp the concept better. "
                           "You always use MathJax to format mathematical expressions.")
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-thinking-exp-1219",
        system_instruction=system_instructions)

    # Additional gemini configuration for chat
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant",
                                      "content": "Come solving faster! Obey your master!...",
                                      "avatar": "res/master_of_numbers.jpg"}]
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(
            history=[
                {"role": "user", "parts": ("Hello! I will send you images of a question and its mark scheme, "
                                           "and then in triple brackets I will say what exactly I don't understand")},
                {"role": "model", "parts": "I will do my best to help you!"},
            ])
    if "first_prompt" not in st.session_state:
        st.session_state.first_prompt = True
    if "last_prompt" not in st.session_state:
        st.session_state.last_prompt = None
    if "open_chat" not in st.session_state:
        st.session_state.open_chat = False

    return model
