#
import streamlit as st
import pandas as pd
from datetime import datetime


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
    recommended_time = question_bank.loc[mask, "marks_available"].values[0] * 1.2
    if st.session_state["time_" + str(i)]:
        time_spent = st.session_state["time_" + str(i)] / recommended_time
        time_spent = time_spent.item()
    else:
        time_spent = "No time recorded"
    question_bank.loc[mask, "marks_gained"] = question_bank.loc[mask, "marks_gained"].apply(
        lambda d: {**d, datetime.today().strftime('%d %b %Y %H:%M'):
            [st.session_state["marks_" + str(i)], time_spent]})
    question_bank.to_csv("res/question_bank.csv")

    # Update progress record
    topic = question_bank.loc[mask, "topic"].values[0]
    topic_bank = question_bank.loc[question_bank["topic"]  == topic]

    marks_available = topic_bank.loc[:, "marks_available"].sum()
    marks_gained = 0

    q_available = topic_bank.loc[:, "marks_available"].count()
    q_attempted = 0

    for marks_dict in topic_bank.loc[:, "marks_gained"]:
        marks_gained += list(marks_dict.values())[-1][0] if marks_dict else 0
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

    # Display a success message
    st.toast(f"Recorded {st.session_state["marks_" + str(i)]} marks", icon="✅")

# Display progress stats for a paper
def display_progress(paper):
    from streamlit_app import question_bank, progress_record
    paper_record = progress_record.loc[progress_record["paper"] == paper]

    # Display paper stats dataframe
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

    # On topic (row) selection: display topic stats
    if st.session_state["stats_" + paper].selection.rows:
        paper_record.reset_index(drop=True, inplace=True)
        topic = paper_record.iat[st.session_state["stats_" + paper].selection.rows[0], 0]

        st.subheader(topic)
        st.markdown(f"""**Marks scored:**
            {round(paper_record.loc[st.session_state["stats_" + paper].selection.rows[0], "marks_scored"] * 100)}%""")
        st.markdown(f"""**Questions attempted:**
            {round(paper_record.loc[st.session_state["stats_" + paper].selection.rows[0], "q_attempted"] * 100)}%""")

        topic_progress = question_bank.loc[question_bank["topic"] == topic]

        topic_stats = pd.DataFrame(data={"Question": [],
                                         "Qualification": [],
                                         "Year": [],
                                         "Attempts": [],
                                         "Last attempted": []})

        for index, question in topic_progress.iterrows():
            topic_stats = pd.concat([topic_stats,
                                     pd.DataFrame(data={"Question": ["Question " + str(index + 1)],
                                                        "Qualification": [question.loc["qualification"]],
                                                        "Year": [question.loc["year"]],
                                                        "Attempts": [len(question.loc["marks_gained"])],
                                                        "Last attempted": [list(question.loc["marks_gained"])[-1]] \
                                                            if question.loc["marks_gained"] else None
                                                        })],
                                    ignore_index=True)

        # Display topic stats dataframe
        st.dataframe(topic_stats,
                     column_config={
                         "Qualification": st.column_config.TextColumn(None, width="small"),
                         "Year": st.column_config.Column(None, width="small"),
                         "Attempts": st.column_config.Column(None, width="small"),
                         "Last attempted": st.column_config.DateColumn(None, width="small")},
                     hide_index=True)
