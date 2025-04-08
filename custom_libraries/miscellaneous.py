#
import streamlit as st
from datetime import datetime


# Customisable sidebar for pages
def sidebar():
    with st.sidebar:
        st.page_link("pages/home.py", label="Home", icon="🏠")
        st.page_link("pages/question_selector.py", label="Question selector", icon="❓")
        st.page_link("pages/revision_session.py", label="Practice papers", icon="📝")
        st.divider()
        st.page_link("pages/progress.py", label="Your account", icon="👤")
        st.button("Log out")
        st.divider()
        st.page_link("pages/about.py", label="About", icon="ℹ️")


# Rerun logging for debugging
def rerun_log():
    if 'run_count' not in st.session_state:
        st.session_state.run_count = 0
    st.session_state.run_count += 1
    print(f"\n--- App Rerun ({st.session_state.run_count}) @ {datetime.now().strftime('%H:%M:%S.%f')} ---")


# SuperMemo 2 algorithm for spaced repetition
def sm_2(grade, n, ef, interval):
    if grade >= 3:
        if n == 0:
            interval = 1
        elif n == 1:
            interval = 6
        else:
            interval = round(interval * ef)
        n +=1
    else:
        n = 0
        interval = 1

    ef = ef + (0.1 - (5-grade)*(0.08 + 0.02*(5-grade)))
    if ef < 1.3: ef = 1.3

    return n, ef, interval


# Record marks in question bank and update progress record
def record_marks(i):
    from streamlit_app import question_bank, progress_record

    # Record marks in question bank
    mask = question_bank["question_path"] == st.session_state.selection[i]
    question_bank.loc[mask, "marks_gained"] = question_bank.loc[mask, "marks_gained"].apply(
        lambda d: {**d, datetime.today().strftime('%Y-%m-%d %H:%M:%S'): st.session_state["marks_" + str(i)]})
    question_bank.to_csv("res/question_bank.csv")

    # Update progress record
    topic = question_bank.loc[mask, "topic"].values[0]
    topic_bank = question_bank.loc[question_bank["topic"]  == topic]

    marks_available = topic_bank.loc[:, "marks_available"].sum()
    marks_gained = 0

    q_available = topic_bank.loc[:, "marks_available"].count()
    q_attempted = 0

    for marks_dict in topic_bank.loc[:, "marks_gained"]:
        marks_gained += list(marks_dict.values())[-1] if marks_dict else 0
        q_attempted += 1 if marks_dict else 0

    marks_percentage = int(marks_gained / marks_available * 100)
    q_percentage = int(q_attempted / q_available * 100)
    n, ef, interval = sm_2(marks_percentage * 5,
                           progress_record.loc[progress_record["topic"] == topic, "n"].values[0],
                           progress_record.loc[progress_record["topic"] == topic, "ef"].values[0],
                           progress_record.loc[progress_record["topic"] == topic, "interval"].values[0])

    progress_record.loc[progress_record["topic"] == topic, "marks_scored":"interval"] = [marks_percentage, q_percentage,
                                                                                         n, ef, interval]
    progress_record.to_csv("res/progress_record.csv")

    st.toast(f"Recorded {st.session_state["marks_" + str(i)]} marks", icon="✅")
