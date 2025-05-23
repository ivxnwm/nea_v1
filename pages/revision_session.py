#
import streamlit as st
from custom_libraries.miscellaneous import sidebar
from streamlit_app import question_bank, progress_record


# Updating search results on filter change
def on_search(query):
    if st.session_state[query]:
        st.session_state.rs_search_query[query] = st.session_state[query]
    else:
        st.session_state.rs_search_query[query] = progress_record.loc[:, query].unique()

# Updating topic selection only if topics are selected manually
def on_topic_selection():
    st.session_state.selection = question_bank[question_bank["topic"].isin(st.session_state.topic_selection)][
        "question_path"].to_list()

# Initial search result is the whole question bank
if "rs_search_result" not in st.session_state:
    st.session_state.rs_search_result = progress_record
if "rs_search_query" not in st.session_state:
    st.session_state.rs_search_query = {
        "qualification": question_bank.loc[:, "qualification"].unique(),
        "paper": question_bank.loc[:, "paper"].unique(),
    }
if "selection" not in st.session_state:
    st.session_state.selection = []


#! --- Page ---
#
sidebar()
st.logo("res/Blueberrevise logo 5.png", size="large")


st.title("Start a revision session")
st.markdown("Revise more efficiently with SuperMemo 2 algorithm! "
            "Select specific areas, or just follow the suggestions &mdash; the algorithm will adapt to your needs.")

# Update revision session search result to match the latest query
st.session_state.rs_search_result = progress_record
for key, value in st.session_state.rs_search_query.items():
    st.session_state.rs_search_result = st.session_state.rs_search_result.loc[st.session_state.rs_search_result[key].isin(value)]
record = st.session_state.rs_search_result.loc[:, ["topic", "interval"]].sort_values(by=["interval"])["topic"].to_list()
if "topic_selection" not in st.session_state:
    for topic in record[:4]:
        st.session_state.selection += question_bank.loc[question_bank["topic"] == topic]["question_path"].to_list()
elif not st.session_state.topic_selection:
    for topic in record[:4]:
        st.session_state.selection += question_bank.loc[question_bank["topic"] == topic]["question_path"].to_list()


# Search filters
st.pills(label="Qualification",
         options=progress_record.loc[:, "qualification"].unique(),
         selection_mode="multi",
         key="qualification",
         args=("qualification",),
         on_change=on_search)
st.pills(label="Paper",
         options=["Core Pure 1", "Further Statistics 1", "Further Mechanics 1", "Decision 1"],
         selection_mode="multi",
         key="paper",
         args=("paper",),
         on_change=on_search)

#
st.markdown(f"For the subjects you've selected SuperMemo 2 suggests to revise these topics: \n"
            f"* {record[0]} \n"
            f"* {record[1]} \n"
            f"* {record[2]} \n"
            f"* {record[3]} \n")
st.write("Press \"Start revising\" to continue with algorithm's suggestions, otherwise, select specific topics to revise:")

# Manual topic selection
st.multiselect(label="Topics",
                    options=question_bank.loc[:, "topic"].unique(),
                    key="topic_selection",
                    placeholder="Select topics",
                    on_change=on_topic_selection)

st.page_link("pages/question_viewer.py", label="Start a session", icon="▶️")
