# Main file that is run, but not rendered
import streamlit as st
import pandas as pd
import ast


# Structure of the app
pages = {
    "Resources": [
        st.Page("pages/home.py", title="Home"),
        st.Page("pages/question_selector.py", title="Questions by topic"),
        st.Page("pages/revision_session.py", title="Revision session"),
    ],
    "Account": [
        st.Page("pages/progress.py", title="Your progress"),
    ],
    "About": [
        st.Page("pages/about.py", title="About"),
    ],
    "Hidden pages": [
        st.Page("pages/question_viewer.py", title="Question viewer"),
    ]
}


# Load question bank and progress record, convert stringified records to Python objects
question_bank = pd.read_csv("res/question_bank.csv", index_col=0)

question_bank.loc[:, "additional_question_paths"] = question_bank.loc[:, "additional_question_paths"].apply(
    lambda x: ast.literal_eval(x))
question_bank.loc[:, "mark_scheme_paths"] = question_bank.loc[:, "mark_scheme_paths"].apply(
    lambda x: ast.literal_eval(x))
question_bank.loc[:, "marks_gained"] = question_bank.loc[:, "marks_gained"].apply(
    lambda x: ast.literal_eval(x))

progress_record = pd.read_csv("res/progress_record.csv", index_col=0)


# Renders the first page
pg = st.navigation(pages, position="hidden")
pg.run()
