#
import pandas as pd
import streamlit as st
from custom_libraries.miscellaneous import sidebar, display_progress
from streamlit_app import question_bank, progress_record

#! --- Page ---
#
sidebar()

st.title("Your progress")


# Display progress stats for each paper and topic (if clicked)
core_pure_tab, stats_tab, mech_tab, decision_tab = st.tabs(["Core Pure", "Statistics", "Mechanics", "Decision"])
with core_pure_tab:
    display_progress("Core Pure 1")
with stats_tab:
    display_progress("Further Statistics 1")
with mech_tab:
    display_progress("Further Mechanics 1")
with decision_tab:
    display_progress("Decision 1")
