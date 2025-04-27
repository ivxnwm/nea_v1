#
import streamlit as st
from datetime import datetime


#! --- Debugging ---
# Rerun logging for debugging
def rerun_log():
    if 'run_count' not in st.session_state:
        st.session_state.run_count = 0
    st.session_state.run_count += 1
    print(f"\n--- App Rerun ({st.session_state.run_count}) @ {datetime.now().strftime('%H:%M:%S.%f')} ---")

#! --- UI/UX ---
# Customisable sidebar for pages
def sidebar():
    with st.sidebar:
        st.page_link("pages/home.py", label="Home", icon="🏠")
        st.page_link("pages/question_selector.py", label="Question selector", icon="❓")
        st.page_link("pages/revision_session.py", label="Revision session", icon="🔄")
        st.page_link("pages/progress.py", label="Your progress", icon="📈")
        st.button("Log out")
        st.divider()
        st.page_link("pages/about.py", label="About", icon="ℹ️")

