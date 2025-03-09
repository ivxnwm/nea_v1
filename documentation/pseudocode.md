# Timers

## Stopwatch

Toggle stopwatch
```
procedure toggle_stopwatch(stopwatch_running, stopwatch_elapsed_time, stopwatch_start_time, current_time)
    if stopwatch_running = true then
        stopwatch_elapsed_time = stopwatch_elapsed_time + (current_time - stopwatch_start_time)
        stopwatch_running = false
    else
        stopwatch_start_time = current_time
        stopwatch_running = true
    endif
endprocedure
```

Reset stopwatch
```
procedure reset_stopwatch(stopwatch_running, stopwatch_start_time, stopwatch_elapsed_time)
    stopwatch_running = false
    stopwatch_start_time = null
    stopwatch_elapsed_time = 0.0
endprocedure
```

Stopwatch display - to be rerun every second - ?
```
procedure stopwatch_display(stopwatch_running, stopwatch_elapsed_time, stopwatch_start_time, current_time)
    if stopwatch_running = true then
        elapsed = stopwatch_elapsed_time + (current_time - stopwatch_start_time)
    else
        elapsed = stopwatch_elapsed_time
    endif
    stopwatch_minutes = int(elapsed DIV 60)
    stopwatch_seconds = int(elapsed MOD 60)
    print(f"{st.session_state.stopwatch_minutes:02} : {st.session_state.stopwatch_seconds:02}")
endprocedure
```

Buttons - ?
```
procedure stopwatch_buttons(stopwatch_running)
    left, right = st.columns(2)
    with left:
        if stopwatch_running = false then
            st.button(":material/play_arrow:", on_click=toggle_stopwatch, key="stopwatch_start_top", use_container_width=true)
        else
            button(":material/pause:", on_click=toggle_stopwatch, key="stopwatch_start_stop", use_container_width=true)
        endif
    with right:
        st.button("Reset", key="stopwatch_reset", on_click=reset_stopwatch, use_container_width=True)
endprocedure
```

## Timer

Toggle timer
```
procedure toggle_timer(timer_first_run, timer_remaining_time, timer_set_time, timer_running)
    if timer_first_run = true then
        timer_remaining_time = timer_set_time * 60
        timer_first_run = false
    endif
    timer_running = not timer_running
endprocedure
```

Reset timer
```
procedure reset_timer(timer_remaining_time, timer_set_time, timer_running, timer_first_run)
    timer_remaining_time = timer_set_time * 60
    timer_running = false
    timer_first_run = true
endprocedure
```

Timer display - to be rerun every second - ?
```
procedure timer_display(timer_running, timer_remaining_time, timer_first_run, timer_set_time)
    if timer_running = true AND timer_remaining_time > 0 then
        timer_remaining_time = timer_remaining_time - 1
    endif
    
    if timer_running = true AND timer_remaining_time = 0 then
        timer_running = false
        timer_first_run = true
        on_timer_end() # customisable function to be called when timer ends
    endif

    timer_minutes = int(timer_remaining_time DIV 60)
    timer_seconds = int(timer_remaining_time MOD 60)

    print(str(timer_minutes) + " : " + str(timer_seconds))
    print("Time Set: " + str(timer_set_time) + " minutes")
endprocedure
```

# Exam clock

Reset exam clock
```
procedure reset_exam(exam_remaining_time, exam_running, exam_first_run, exam_set_time)
    exam_remaining_time = timedelta(minutes = exam_set_time)
    exam_running = false
    exam_first_run = true
endprocedure
```

Toggle exam clock
```
procedure toggle_exam(exam_first_run, exam_remaining_time, exam_running, exam_start_time, exam_end_time, exam_set_time, current_time)
    if exam_first_run = true then
        exam_remaining_time = timedelta(minutes = exam_set_time)
        exam_first_run = false
        exam_start_time = current_time
    endif
    
    if exam_running = true then
        exam_remaining_time = exam_end_time - current_time
    else
        exam_end_time = current_time + exam_remaining_time
    endif

    exam_running = NOT exam_running
endprocedure
```

Display exam clock - ?
```
procedure exam_display(exam_end_time, exam_start_time, exam_running, exam_first_run, current_time)
    if exam_end_time != null AND current_time < exam_end_time then
        print("Start" + exam_start_time.strftime("%H:%M"))
        print("Finish" + exam_end_time.strftime("%H:%M"))
    elseif exam_end_time != null AND current_time = exam_end_time then
        exam_running = false
        exam_first_run = true
        on_exam_end()
    endif
    
    print(current_time.strftime("%H:%M"))
endprocedure
```

# Chatbot

Display messages
```
for message in messages do
    print(message["role"] + message["content"])
next message
```

Prompt input
```
procedure prompt_input(prompt, messages, first_prompt)
    if prompt != null then
        messages.append({"role": "user", "content": prompt})
        
        if first_prompt = true then
            open_chat = true
            first_prompt = prompt
        else
            last_prompt = prompt
        endif
        
        return first_prompt, last_prompt, open_chat
    endif
endprocedure
```

Generate response if last message is not from assistant
```
procedure generate_seponce(messages, first_prompt, last_prompt, question, mark_scheme)
    if messages[-1]["role"] != "assistant" then
        // For the first user message, include question and mark scheme
        if first_prompt = true then
            full_prompt = [question, mark_scheme, "'''" + first_prompt + "'''"]
            first_prompt = false
        elseif last_prompt != null then
            full_prompt = [last_prompt]
        endif
    
        response = chat.send_message(content = full_prompt, stream = true) // calling Gemini API
        response.resolve() // Response is generated in 'chunks' which come one by one, so we can start displaying already received chunks before receiving full response
        
        full_response = ""
        for chunk in response.text do
            full_response = full_response + chunk
            print(full_response)
        next chunk
        
        print(full_response)
        messages.append({"role": "assistant", "content": full_response})
    endif
endprocedure
```