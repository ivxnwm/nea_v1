#
import streamlit as st
import PIL.Image as im
from custom_libraries import timers, miscellaneous, progress_tracking, chatbot
from streamlit_app import question_bank
from streamlit_extras.stylable_container import stylable_container


# Rerun logging for debugging
miscellaneous.rerun_log()


# Gemini chat configuration
model = chatbot.gemini_configuration()


# Initialise timers
timers.initialise_stopwatch()
timers.initialise_timer()
timers.initialise_exam()

# Initialise fragments for timers display (to only rerun the timer display)
@st.fragment(run_every=0.2 if st.session_state.stopwatch_running else None)
def stopwatch_display():
    timers.stopwatch_display()

@st.fragment(run_every=1 if st.session_state.timer_running else None)
def timer_display():
    timers.timer_display()

@st.fragment(run_every=1)
def exam_display():
    timers.exam_display()


#! --- Page ---
#
st.set_page_config(layout="wide")
miscellaneous.sidebar()
st.logo("res/Blueberrevise logo 5.png", size="large")
if st.session_state.open_chat:
    col1, col2 = st.columns([0.45, 0.55])
else:
    col1, col2 = st.columns([0.7, 0.3])

# Question resources
with col1:
    if "selection" in st.session_state:
        questions = []
        mark_schemes = []
        for i in range(len(st.session_state.selection)):
            with stylable_container(key="question_container_" + str(i),
                                    css_styles="""{background-color: #f5f7fb;
                                                   border-radius: 1.2rem;
                                                   padding: calc(1em - 1px)
                                                   }""",
            ):

                curr = question_bank.loc[question_bank["question_path"] == st.session_state.selection[i]].replace(
                    {float('nan'): None})
                content = {"Question": [curr.loc[:, "question_path"].values[0] + r".jpg"]
                                       + curr.loc[:, "additional_question_paths"].values[0],
                           "Mark scheme": curr.loc[:, "mark_scheme_paths"].values[0],
                           "Examiner's report": curr.loc[:, "examiners_report"].values[0],
                           "Model answer": curr.loc[:, "model_answer_link"].values[0],
                           "Record marks and time": curr.loc[:, "marks_available"].values[0]}

                st.header(f"Question {i+1}")
                st.markdown(
                    f""":violet-badge[{curr.loc[:, "qualification"].values[0]}]
                        :orange-badge[{curr.loc[:, "paper"].values[0]}]
                        :gray-badge[{curr.loc[:, "year"].values[0]}]
                        :blue-badge[{curr.loc[:, "topic"].values[0]}]
                        Recommended time: {round(curr.loc[:, "marks_available"].values[0] * 1.2)} minutes"""
                )

                question_tab, mark_scheme_tab, e_r_tab, m_a_tab, marks_tab = st.tabs(content.keys())
                with question_tab:
                    for page in content["Question"]:
                        questions.append(im.open(r"res/" + page))
                        st.image(questions[-1], use_container_width=True)
                with mark_scheme_tab:
                    for page in content["Mark scheme"]:
                        mark_schemes.append(im.open(r"res/" + page))
                        st.image(mark_schemes[-1], use_container_width=True)
                with e_r_tab:
                    if content["Examiner's report"]:
                        st.markdown(content["Examiner's report"])
                    else:
                        st.write("Not available")
                with m_a_tab:
                    if content["Model answer"]:
                        st.write("Unfortunately, we are unable to display PMT model answers here due to copyright, "
                                 "but here is the link to the file on PMT website:")
                        st.write(content["Model answer"])
                    else:
                        st.write("Not available")
                with marks_tab:

                    left, right = st.columns(2)
                    with left:
                        st.number_input(label="Record marks you gained to keep track of your progress",
                                        min_value=0, max_value=content["Record marks and time"],
                                        key="marks_" + str(i))
                        st.number_input(label="Record time you spent on this question (optional)",
                                        min_value=1, max_value=180, value=None,
                                        key="time_" + str(i),
                                        placeholder="Time spent (minutes)")
                        st.button("Record marks and time",
                                  args=(i,), on_click=progress_tracking.record_marks,
                                  key="record_marks_" + str(i))
                    with right:
                        with st.expander("Previous attempts", expanded=True):
                            if curr.loc[:, "marks_gained"].values[0] == {}:
                                st.write("No previous attempts")
                            else:
                                for record in curr.loc[:, "marks_gained"].values[0]:
                                    st.markdown(f"{record}: "
                                                f"**{curr.loc[:, "marks_gained"].values[0][record][0]} marks**")
                                    if isinstance(curr.loc[:, "marks_gained"].values[0][record][1], float):
                                        st.caption(f"Time spent: "
                                                   f"{round(curr.loc[:, "marks_gained"].values[0][record][1] * 100)}"
                                                   f"% of recommended")
                                    else:
                                        st.caption("No time recorded")
    else:
        st.warning("""
        No question selected.  
        Please select a question from the Question Selector page to view it here.
        """)

with col2:
    #! --- Timers ---
    #
    timer_selection = st.segmented_control("Select timer", ["Stopwatch", "Timer", "Exam clock"],
                               selection_mode="single",
                               default=None,
                               label_visibility="collapsed")
    # Stopwatch
    if timer_selection == "Stopwatch":
        stopwatch_display()
        timers.stopwatch_buttons()
    # Timer
    elif timer_selection == "Timer":
        st.session_state.timer_set_time = st.number_input("Set timer (minutes)", min_value=1, max_value=180, step=1)
        timer_display()
        timers.timer_buttons()
    # Exam clock
    elif timer_selection == "Exam clock":
        st.session_state.exam_set_time = st.number_input("Set exam time (minutes)",
                                                         min_value=15, max_value=180, step=15)
        exam_display()
        timers.exam_buttons()
    st.divider()


    #! ---Chatbot---
    #
    with st.container(height=600, border=True):
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=message["avatar"]):
                st.write(message["content"])

        # Generate response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            # For the first user message, include question and mark scheme
            if st.session_state.first_prompt:
                full_prompt = questions + mark_schemes + ["'''" + st.session_state.first_prompt + "'''"]
            elif st.session_state.last_prompt:
                full_prompt = [st.session_state.last_prompt]

            with st.chat_message("assistant", avatar=None):
                with st.spinner("Thinking"):
                    response = st.session_state.chat.send_message(content=full_prompt, stream=True)
                    response.resolve()
                    temp = st.empty()
                    full_response = ""
                    for chunk in response.text:
                        full_response += chunk
                        temp.markdown(full_response)
                    temp.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response, "avatar": None})

            st.session_state.first_prompt = False

    # Prompt input
    if prompt := st.chat_input("Send a message"):
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": None})
        if st.session_state.first_prompt:
            st.session_state.open_chat = True
            st.session_state.first_prompt = prompt
            st.rerun()
        else:
            st.session_state.last_prompt = prompt
        st.rerun()
