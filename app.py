import streamlit as st

from chat_engine import load_question_answers, get_response, DEFAULT_RESPONSE


# Initialize chat engine
if 'engine_init' not in st.session_state:
    st.session_state.question_answers = load_question_answers()
    st.session_state.engine_init = True

# Initialize page layout
chat_container = st.container(border=True, height=500)

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    chat_container.chat_message(message['role']).markdown(message['content'])

# Accept user input
if question := st.chat_input('Type a new question...'):
    chat_container.chat_message('user').markdown(question)
    st.session_state.messages.append({'role': 'user', 'content': question})

    with chat_container:
        with st.spinner("Retrieving and generating response."):
            try:
                response = get_response(question, st.session_state.question_answers)
            except Exception as e:
                print(e)
                response = DEFAULT_RESPONSE

            chat_container.chat_message('assistant').markdown(response)
            st.session_state.messages.append({'role': 'assistant', 'content': response})

