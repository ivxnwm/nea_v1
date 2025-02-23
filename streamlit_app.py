import streamlit as st


pages = {
    "Resources": [
        st.Page("home.py", title="Home"),
        st.Page("questions_by_topic.py", title="Questions by topic"),
        st.Page("practice_papers.py", title="Practice papers"),
    ],
    "Account": [
        st.Page("account.py", title="Your account"),
    ],
    "Question_viewer": [
        st.Page("question_viewer.py", title="Question viewer"),
    ],
}

pg = st.navigation(pages, position="hidden")
pg.run()
