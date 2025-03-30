import streamlit as st
import pandas as pd
import ast

pages = {
    "Resources": [
        st.Page("pages/home.py", title="Home"),
        st.Page("pages/question_selector.py", title="Questions by topic"),
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

question_bank = pd.read_csv("res/question_bank.csv", index_col=0)

question_bank.loc[:, "additional_question_paths"] = question_bank.loc[:, "additional_question_paths"].apply(
    lambda x: ast.literal_eval(x))
question_bank.loc[:, "mark_scheme_paths"] = question_bank.loc[:, "mark_scheme_paths"].apply(
    lambda x: ast.literal_eval(x))
question_bank.loc[:, "marks_gained"] = question_bank.loc[:, "marks_gained"].apply(
    lambda x: ast.literal_eval(x))

pg = st.navigation(pages, position="hidden")
pg.run()
