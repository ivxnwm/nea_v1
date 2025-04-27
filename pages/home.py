#
import streamlit as st
from custom_libraries.miscellaneous import sidebar

sidebar()
st.logo("res/Blueberrevise logo 5.png", size="large")


st.title("Home")

st.markdown("On this website you can:")

st.page_link("pages/question_selector.py", label="Select questions", icon="❓")
st.page_link("pages/progress.py", label="Track your progress", icon="📈")
st.page_link("pages/revision_session.py", label="Start a revision session, where algorithm selects most relevant questions", icon="🔄")

st.write("""
While doing a question, you can also:  
⏱️ Time your revision work with a stopwatch, timer or a clock just like in a real exam  
🤖 Ask the most advanced Gemini model anything about the question
""")
