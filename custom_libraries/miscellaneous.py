#
import streamlit as st
from datetime import datetime


# Customisable sidebar for pages
def sidebar():
    with st.sidebar:
        st.page_link("home.py", label="Home", icon="🏠")
        st.page_link("questions_by_topic.py", label="Questions by topic", icon="❓")
        st.page_link("practice_papers.py", label="Practice papers", icon="📝")
        st.divider()
        st.page_link("account.py", label="Your account", icon="👤")
        st.button("Log out")


# Rerun logging for debugging
def rerun_log():
    if 'run_count' not in st.session_state:
        st.session_state.run_count = 0
    st.session_state.run_count += 1
    print(f"\n--- App Rerun ({st.session_state.run_count}) @ {datetime.now().strftime('%H:%M:%S.%f')} ---")