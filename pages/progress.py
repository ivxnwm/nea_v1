import pandas as pd
import streamlit as st
from custom_libraries.miscellaneous import sidebar
from streamlit_app import question_bank, progress_record


sidebar()

st.title("Your progress")


def display_stats(paper):
    paper_record = progress_record.loc[progress_record["paper"] == paper]

    st.dataframe(paper_record.loc[:, ["topic", "marks_scored", "q_attempted"]], use_container_width=True,
                 column_config={
                     "topic": st.column_config.TextColumn("Topic"),
                     "marks_scored": st.column_config.ProgressColumn("Marks scored", width="small",
                         help="Total percentage of marks gained for all questions on this topic",
                         format="%d%%", min_value=0, max_value=100),
                     "q_attempted": st.column_config.ProgressColumn("Questions attempted", width="small",
                          help="Total percentage of questions attempted on this topic",
                          format="%d%%", min_value=0, max_value=100)},
                 hide_index=True,
                 key="stats_" + paper,
                 on_select="rerun",
                 selection_mode="single-row")

    if st.session_state["stats_" + paper].selection.rows:
        paper_record.reset_index(drop=True, inplace=True)
        topic = paper_record.iat[st.session_state["stats_" + paper].selection.rows[0], 0]
        st.subheader(topic)
        st.markdown(f"""**Marks scored:**
            {round(paper_record.loc[st.session_state["stats_" + paper].selection.rows[0], "marks_scored"] * 100)}%""")
        st.markdown(f"""**Questions attempted:**
            {round(paper_record.loc[st.session_state["stats_" + paper].selection.rows[0], "q_attempted"] * 100)}%""")

        topic_bank = question_bank.loc[question_bank["topic"] == topic]

        topic_stats = pd.DataFrame(data={"Question": [],
                                         "Qualification": [],
                                         "Year": [],
                                         "Attempts": [],
                                         "Last attempted": []})

        for index, question in topic_bank.iterrows():
            topic_stats = pd.concat([topic_stats,
                                     pd.DataFrame(data={"Question": ["Question " + str(index + 1)],
                                                        "Qualification": [question.loc["qualification"]],
                                                        "Year": [question.loc["year"]],
                                                        "Attempts": [len(question.loc["marks_gained"])],
                                                        "Last attempted": [list(question.loc["marks_gained"])[-1]] \
                                                            if question.loc["marks_gained"] else None
                                                        })],
                                    ignore_index=True)

        st.dataframe(topic_stats,
                     column_config={
                         "Qualification": st.column_config.TextColumn(None, width="small"),
                         "Year": st.column_config.Column(None, width="small"),
                         "Attempts": st.column_config.Column(None, width="small"),
                         "Last attempted": st.column_config.DateColumn(None, width="small")},
                     hide_index=True)


core_pure_tab, stats_tab, mech_tab, decision_tab = st.tabs(["Core Pure", "Statistics", "Mechanics", "Decision"])
with core_pure_tab:
    display_stats("Core Pure 1")
with stats_tab:
    display_stats("Further Statistics 1")
with mech_tab:
    display_stats("Further Mechanics 1")
with decision_tab:
    display_stats("Decision 1")
