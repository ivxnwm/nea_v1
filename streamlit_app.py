import streamlit as st
import pandas as pd


pages = {
    "Resources": [
        st.Page("pages/home.py", title="Home"),
        st.Page("pages/questions_by_topic.py", title="Questions by topic"),
        st.Page("pages/practice_papers.py", title="Practice papers"),
    ],
    "Account": [
        st.Page("pages/account.py", title="Your account"),
    ],
    "About": [
        st.Page("pages/about.py", title="About"),
    ],
    "Question_viewer": [
        st.Page("pages/question_viewer.py", title="Question viewer"),
    ]
}

pg = st.navigation(pages, position="hidden")
pg.run()
