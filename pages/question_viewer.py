#
import streamlit as st
import PIL.Image as im
from custom_libraries import timers, miscellaneous, chatbot

# Rerun logging for debugging
miscellaneous.rerun_log()


# Gemini chat configuration
model = chatbot.gemini_configuration()


# Temp
question = im.open(r"res/question_1.webp")
mark_scheme = im.open(r"res/mark_scheme_1.png")
PROMPT = "I don't understand how to do this question, explain it to me step by step"


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
st.set_page_config(layout="wide")
miscellaneous.sidebar()
if st.session_state.open_chat:
    col1, col2 = st.columns([0.45, 0.55])
else:
    col1, col2 = st.columns([0.7, 0.3])


with col1:
    # Question resources
    st.header("Paper 1 Q1 2025")
    content = {"Question": question, "Mark scheme": mark_scheme, "Examiner's report": None, "Model answer": None}
    question_tab, mark_scheme_tab, e_r_tab, m_a_tab = st.tabs(content.keys())
    with question_tab:
        st.image(question, use_container_width=True)
    with mark_scheme_tab:
        st.image(mark_scheme, use_container_width=True)
    with e_r_tab:
        st.write("Not available")
    with m_a_tab:
        st.write("Not available")

    # Record marks
    marks_available = 10
    left, right = st.columns(2)
    with left:
        marks = st.number_input(label="Record how many marks you gained to keep track of your progress", min_value=0, max_value=marks_available, placeholder="Marks gained")
    with right:
        st.button("Record marks", on_click=None, disabled=(not marks))


with col2:
    #! --- Timers ---
    timer_selection = st.segmented_control("Select timer", ["Stopwatch", "Timer", "Exam clock"],
                               selection_mode="single",
                               default=None,
                               label_visibility="collapsed")
    if timer_selection == "Stopwatch":
        # Stopwatch
        stopwatch_display()
        timers.stopwatch_buttons()
    elif timer_selection == "Timer":
        # Timer
        st.session_state.timer_set_time = st.number_input("Set timer (minutes)", min_value=1, max_value=180, step=1)
        timer_display()
        timers.timer_buttons()
    elif timer_selection == "Exam clock":
        # Exam clock
        st.session_state.exam_set_time = st.number_input("Set exam time (minutes)",
                                                         min_value=15, max_value=180, step=15)
        exam_display()
        timers.exam_buttons()

    #! ---Chatbot---
    with st.container(height=300, border=True):
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=message["avatar"]):
                st.write(message["content"])

        # Generate response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            # For the first user message, include question and mark scheme
            if st.session_state.first_prompt:
                full_prompt = [question, mark_scheme, "'''" + st.session_state.first_prompt + "'''"]
                st.session_state.first_prompt = False
            elif st.session_state.last_prompt:
                full_prompt = [st.session_state.last_prompt]

            with st.chat_message("assistant", avatar="res/master_of_numbers.jpg"):
                with st.spinner("Thinking"):
                    response = st.session_state.chat.send_message(content=full_prompt, stream=True)
                    response.resolve()
                    temp = st.empty()
                    full_response = ""
                    for chunk in response.text:
                        full_response += chunk
                        temp.markdown(full_response)
                    temp.markdown(full_response)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": full_response, "avatar": "res/master_of_numbers.jpg"})

    # Prompt input
    if prompt := st.chat_input("Ask Master of Numbers"):
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": None})
        if st.session_state.first_prompt:
            st.session_state.open_chat = True
            st.session_state.first_prompt = prompt
            st.rerun()
        else:
            st.session_state.last_prompt = prompt
        st.rerun()
