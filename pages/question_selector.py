import streamlit as st
from custom_libraries.miscellaneous import sidebar, rerun_log
from streamlit_app import question_bank
from streamlit_extras.stylable_container import stylable_container


st.set_page_config(page_title="Blueberrevise", page_icon="🫐", layout="wide", menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

# Rerun logging for debugging
rerun_log()

sidebar()

st.title("Question selector")

# Debugging
# st.dataframe(question_bank)
# st.session_state


if "search_result" not in st.session_state:
    st.session_state.search_result = question_bank
if "search_query" not in st.session_state:
    st.session_state.search_query = {
        "qualification": question_bank.loc[:, "qualification"].unique(),
        "paper": question_bank.loc[:, "paper"].unique(),
        "year": question_bank.loc[:, "year"].unique(),
        "topic": question_bank.loc[:, "topic"].unique()
    }
if "selection" not in st.session_state:
    st.session_state.selection = []

st.session_state.search_result = question_bank
for key, value in st.session_state.search_query.items():
    st.session_state.search_result = st.session_state.search_result.loc[st.session_state.search_result[key].isin(value)]

def on_search(query):
    if st.session_state[query]:
        st.session_state.search_query[query] = st.session_state[query]
    else:
        st.session_state.search_query[query] = question_bank.loc[:, query].unique()

def on_selection():
    st.session_state.selection = []
    for i in range(len(st.session_state.search_result)):
        if st.session_state["selection_" + str(i)]:
            st.session_state.selection.append(st.session_state.search_result.iat[i, 0])

left, right = st.columns([0.6, 0.4])
with left:
    st.multiselect(label="Topics",
                    options=question_bank.loc[:, "topic"].unique(),
                    key="topic",
                    placeholder="Select topics",
                    args=("topic",),
                    on_change=on_search)
    st.pills(label="Qualification",
            options=question_bank.loc[:, "qualification"].unique(),
            selection_mode="multi",
            key="qualification",
            args=("qualification",),
            on_change=on_search)
    st.pills(label="Paper",
            options=question_bank.loc[:, "paper"].unique(),
            selection_mode="multi",
            key="paper",
            args=("paper",),
            on_change=on_search)
    st.pills(label="Year",
            options=question_bank.loc[:, "year"].unique(),
            selection_mode="multi",
            key="year",
            args=("year",),
            on_change=on_search)
with right:
    with stylable_container(
        key="current_selection_container",
        css_styles="""
            {
                background-color: #f5f7fb;
                border-radius: 1.2rem;
                padding: calc(1em - 1px)
            }
            """,
    ):
        st.subheader("Current selection")
        if st.session_state.selection:
            with stylable_container(
                key="current_selection_list_container",
                css_styles="""
                    {
                        background-color: #fafdff;
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                    }
                    """,
            ):
                for element in st.session_state.selection:
                    st.write(f"{question_bank.loc[question_bank['question_path'] == element, "year"].values[0]} "
                             f"{question_bank.loc[question_bank['question_path'] == element, "qualification"].values[0]} "
                             f"{question_bank.loc[question_bank['question_path'] == element, "paper"].values[0]} "
                             f"Question {element[15:16]} ")
        with st.container():
            if st.session_state.selection:
                st.button("Clear selection",
                          key="clear_selection_button",
                          on_click=lambda: st.session_state.update({"selection": []}),
                          use_container_width=True)
            st.button("Select all",
                      key="select_all_button",
                      on_click=lambda: st.session_state.update({"selection": st.session_state.search_result["question_path"].tolist()}),
                      use_container_width=True)
            st.page_link("pages/question_viewer.py",
                     label="Start practicing",
                     icon="📝",
                     disabled=not st.session_state.selection,
                     use_container_width=True)

grid = st.columns(3)
col = 0
for i in range(len(st.session_state.search_result)):
    with grid[col]:
        with stylable_container(
            key="search_result_container_"+str(i),
            css_styles="""
            {
                background-color: #f5f7fb;
                border-radius: 1.2rem;
                padding: calc(1em - 1px)
            }
            """,
        ):
            with st.container():
                st.image(r"res/" + st.session_state.search_result.iat[i, 0] + r".jpg")
            st.write(st.session_state.search_result.iat[i, 10])
            st.markdown(
                f""":violet-badge[{st.session_state.search_result.iat[i, 5]}]
                :orange-badge[{st.session_state.search_result.iat[i, 8]}]
                :gray-badge[{st.session_state.search_result.iat[i, 9]}]"""
            )
            st.checkbox("Select this question", key="selection_" + str(i), on_change=on_selection)
    col = (col + 1) % 3
