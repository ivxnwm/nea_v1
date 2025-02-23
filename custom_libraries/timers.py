#
import streamlit as st
import time
from datetime import datetime, timedelta


#! --- Stopwatch ---
# Initialise stopwatch variables
def initialise_stopwatch():
    if "stopwatch_start_time" not in st.session_state:
        st.session_state.stopwatch_start_time = None
    if "stopwatch_running" not in st.session_state:
        st.session_state.stopwatch_running = False
    if "stopwatch_elapsed_time" not in st.session_state:
        st.session_state.stopwatch_elapsed_time = 0.0
    if "stopwatch_minutes" not in st.session_state:
        st.session_state.stopwatch_minutes = 0
    if "stopwatch_seconds" not in st.session_state:
        st.session_state.stopwatch_seconds = 0


def toggle_stopwatch():
    if st.session_state.stopwatch_running:
        st.session_state.stopwatch_elapsed_time += time.time() - st.session_state.stopwatch_start_time
        st.session_state.stopwatch_running = False
    else:
        st.session_state.stopwatch_start_time = time.time()
        st.session_state.stopwatch_running = True


def reset_stopwatch():
    st.session_state.stopwatch_running = False
    st.session_state.stopwatch_start_time = None
    st.session_state.stopwatch_elapsed_time = 0.0


def stop_stopwatch():
    if st.session_state.stopwatch_running:
        st.session_state.stopwatch_elapsed_time = time.time() - st.session_state.stopwatch_start_time
        st.session_state.stopwatch_running = False


# Display stopwatch - to be placed inside st.fragment to only rerun this part (run_every=1)
def stopwatch_display():
    if st.session_state.stopwatch_running:
        elapsed = st.session_state.stopwatch_elapsed_time + (time.time() - st.session_state.stopwatch_start_time)
    else:
        elapsed = st.session_state.stopwatch_elapsed_time
    st.session_state.stopwatch_minutes = int(elapsed // 60)
    st.session_state.stopwatch_seconds = int(elapsed % 60)
    st.title(f"{st.session_state.stopwatch_minutes:02} : {st.session_state.stopwatch_seconds:02}")


def stopwatch_buttons():
    left, right = st.columns(2)
    with left:
        st.button(":material/play_arrow:" if not st.session_state.stopwatch_running else ":material/pause:",
                  on_click=toggle_stopwatch,
                  key="stopwatch_start_top",
                  use_container_width=True)
    with right:
        st.button("Reset", key="stopwatch_reset", on_click=reset_stopwatch, use_container_width=True)


#! --- Timer ---
# Initialise timer variables
def initialise_timer():
    if "timer_set_time" not in st.session_state:
        st.session_state.timer_set_time = 1  # Default to 1 minute
    if "timer_remaining_time" not in st.session_state:
        st.session_state.timer_remaining_time = st.session_state.timer_set_time * 60
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    if "timer_minutes" not in st.session_state:
        st.session_state.timer_minutes = 0
    if "timer_seconds" not in st.session_state:
        st.session_state.timer_seconds = 0
    if "timer_first_run" not in st.session_state:
        st.session_state.timer_first_run = True


def reset_timer():
    st.session_state.timer_remaining_time = st.session_state.timer_set_time * 60
    st.session_state.timer_running = False
    st.session_state.timer_first_run = True


def toggle_timer():
    if st.session_state.timer_first_run:
        st.session_state.timer_remaining_time = st.session_state.timer_set_time * 60
        st.session_state.timer_first_run = False
    st.session_state.timer_running = not st.session_state.timer_running


# Function to run when timer ends - to be customised
def on_timer_end():
    st.balloons()
    time.sleep(3)


# Display timer - to be placed inside st.fragment to only rerun this part (run_every=1)
def timer_display():
    if st.session_state.timer_running and st.session_state.timer_remaining_time > 0:
        st.session_state.timer_remaining_time -= 1
    if st.session_state.timer_running and st.session_state.timer_remaining_time == 0:
        st.session_state.timer_running = False
        st.session_state.timer_first_run = True
        on_timer_end()
        st.rerun()
    st.session_state.timer_minutes = int(st.session_state.timer_remaining_time // 60)
    st.session_state.timer_seconds = int(st.session_state.timer_remaining_time % 60)
    st.title(f"{st.session_state.timer_minutes:02} : {st.session_state.timer_seconds:02}")
    st.write(f"Time Set: {st.session_state.timer_set_time} minutes")


def timer_buttons():
    left, right = st.columns(2)
    with left:
        st.button(":material/play_arrow:" if not st.session_state.timer_running else ":material/pause:",
                  on_click=toggle_timer,
                  key="timer_start_top",
                  use_container_width=True)
    with right:
        st.button("Reset", key="timer_reset", on_click=reset_timer, use_container_width=True)


#! --- Exam clock ---
# Initialise exam clock variables
def initialise_exam():
    if "exam_set_time" not in st.session_state:
        st.session_state.exam_set_time = 1  # Default to 1 hour
    if "exam_start_time" not in st.session_state:
        st.session_state.exam_start_time = None
    if "exam_end_time" not in st.session_state:
        st.session_state.exam_end_time = None
    if "exam_remaining_time" not in st.session_state:
        st.session_state.exam_remaining_time = None
    if "exam_running" not in st.session_state:
        st.session_state.exam_running = False
    if "exam_first_run" not in st.session_state:
        st.session_state.exam_first_run = True


def reset_exam():
    st.session_state.exam_remaining_time = timedelta(minutes=st.session_state.exam_set_time)
    st.session_state.exam_running = False
    st.session_state.exam_first_run = True


def toggle_exam():
    if st.session_state.exam_first_run:
        st.session_state.exam_remaining_time = timedelta(minutes=st.session_state.exam_set_time)
        st.session_state.exam_first_run = False
        st.session_state.exam_start_time = datetime.now()
    if st.session_state.exam_running:
        st.session_state.exam_remaining_time = st.session_state.exam_end_time - datetime.now()
    else:
        st.session_state.exam_end_time = datetime.now() + st.session_state.exam_remaining_time
    st.session_state.exam_running = not st.session_state.exam_running


# Function to run when exam ends - to be customised
def on_exam_end():
    st.balloons()
    time.sleep(3)


# Display exam clock - to be placed inside st.fragment to only rerun this part (run_every=1)
def exam_display():
    now = datetime.now()
    if st.session_state.exam_end_time and now < st.session_state.exam_end_time:
        left, right = st.columns(2)
        with left:
            st.metric("Start", st.session_state.exam_start_time.strftime("%H:%M"))
        with right:
            st.metric("Finish", st.session_state.exam_end_time.strftime("%H:%M"))
    elif st.session_state.exam_end_time and now == st.session_state.exam_end_time:
        st.session_state.exam_running = False
        st.session_state.exam_first_run = True
        on_exam_end()
        st.rerun()
    st.title(now.strftime("%H:%M"))


def exam_buttons():
    left, right = st.columns(2)
    with left:
        st.button(" :material/play_arrow:" if not st.session_state.exam_running else ":material/pause:",
                  on_click=toggle_exam,
                  key="exam_start_top",
                  use_container_width=True)
    with right:
        st.button("Reset", key="exam_reset", on_click=reset_exam, use_container_width=True)
