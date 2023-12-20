import streamlit as st
import numpy as np
from qa import get_response

PROFESSOR_LIST = ["廖世偉", "林軒田"]


def input_box():
    question = st.chat_input("Say something")
    if question:
        answer = get_response(question, st.session_state.answer)
        st.session_state.qa_logs.append((question, answer))


def show_logs():
    with st.container():
        for prompt, answer in st.session_state.qa_logs:
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("ai"):
                st.write(answer)


def main():
    if "qa_logs" not in st.session_state:
        st.session_state.qa_logs = []

    if "answer" not in st.session_state:
        st.session_state.answer = np.random.choice(PROFESSOR_LIST)

    st.title("明資顧問")

    input_box()

    show_logs()


if __name__ == "__main__":
    main()
