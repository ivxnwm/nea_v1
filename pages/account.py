import pandas as pd
import streamlit as st
from custom_libraries.miscellaneous import sidebar
from streamlit_app import question_bank
from streamlit_extras.stylable_container import stylable_container


sidebar()

st.title("Your account")


paper_bank = {}

marks_available = {}
marks_gained = {}
marks_percentage = {}

q_available = {}
q_attempted = {}
q_percentage = {}

def display_stats(paper):
    global paper_bank, marks_available, marks_gained, marks_percentage, q_attempted
    stats = pd.DataFrame(data={"Topic": [], "Marks scored": [], "Questions attempted": []})

    if paper == "Core Pure 1":
        paper_bank[paper] = question_bank.loc[question_bank["paper"].isin(["Core Pure 1", "Core Pure 2"])]
    else:
        paper_bank[paper] = question_bank.loc[question_bank["paper"].isin([paper])]

    marks_available[paper] = {}
    marks_gained[paper] = {}
    marks_percentage[paper] = {}

    q_available[paper] = {}
    q_attempted[paper] = {}
    q_percentage[paper] = {}

    for topic in paper_bank[paper].loc[:, "topic"].unique():
        marks_available[paper][topic] = paper_bank[paper].loc[
            paper_bank[paper]["topic"] == topic, "marks_available"].sum()
        marks_gained[paper][topic] = 0

        q_available[paper][topic] = paper_bank[paper].loc[
            paper_bank[paper]["topic"] == topic, "marks_available"].count()
        q_attempted[paper][topic] = 0

        for marks_dict in paper_bank[paper].loc[paper_bank[paper]["topic"] == topic, "marks_gained"]:
            marks_gained[paper][topic] += marks_dict[marks_dict.keys()[-1]] if topic in marks_dict else 0
            q_attempted[paper][topic] += 1 if marks_dict else 0

        marks_percentage[paper][topic] = int(marks_gained[paper][topic] / marks_available[paper][topic] * 100)
        q_percentage[paper][topic] = int(q_attempted[paper][topic] / q_available[paper][topic] * 100)

        stats = pd.concat([stats, pd.DataFrame(data={"Topic": [topic],
                                                    "Marks scored": [marks_percentage[paper][topic]],
                                                    "Questions attempted": [q_percentage[paper][topic]]})],
                                                    ignore_index=True)

    st.dataframe(stats, use_container_width=True,
                 column_config={
                     "Marks scored": st.column_config.ProgressColumn(None, width="small",
                                    help="Total percentage of marks gained for all questions on this topic",
                                    format="%d%%", min_value=0, max_value=100),
                     "Questions attempted": st.column_config.ProgressColumn(None, width="small",
                                    help="Total percentage of questions attempted on this topic",
                                    format="%d%%", min_value=0, max_value=100)},
                 hide_index=True,
                 key="stats_" + paper,
                 on_select="ignore",
                 selection_mode="single-row")


core_pure_tab, stats_tab, mech_tab, decision_tab = st.tabs(["Core Pure", "Statistics", "Mechanics", "Decision"])
with core_pure_tab:
    display_stats("Core Pure 1")
with stats_tab:
    display_stats("Further Statistics 1")
with mech_tab:
    display_stats("Further Mechanics 1")
with decision_tab:
    display_stats("Decision 1")
