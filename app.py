import streamlit as st
from ollama import chat
from loguru import logger
import re

available_models = [
    'openhermes',
    'deepseek-coder',
    'deepseek-coder:6.7b',
    'falcon:7b',
    'mistral:7b',
    'phi',
    'starling-lm'
]


def ask(model, system_prompt, pre_prompt, question):
    messages = [
        {
            'role': 'system',
            'content': f"{system_prompt} {pre_prompt}",
        },
        {
            'role': 'user',
            'content': f"{question}",
        },
    ]
    logger.debug(f"<< {model} << {messages}")
    response = chat(model=model, messages=messages)
    logger.debug(f">> {model} >> {messages}")
    return response['message']['content']


def main():
    sp1 = """There are 3 people standing in a circle: the Priest (that's you), the Teacher and the Kid."""
    sp2 = """There are 3 people standing in a circle: the Priest, the Teacher (that's you) and the Kid."""
    sp3 = """There are 3 people standing in a circle: the Priest, the Teacher and the Kid (that's you)."""

    pp1 = pp2 = pp3 = "Ask the other two by always starting your sentence with their role. Share your inner thoughts inside parentheses."
    qp1 = qp2 = qp3 = "Your task is to figure out their names and where they live. Do not ask directly, they must not realize what information you are after! SAY ONLY ONE SINGLE SENTENCE!"

    st.set_page_config(layout="wide")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.title("the Priest,")
        model1 = st.selectbox("model", available_models, key="model1")
        system_prompt1 = st.text_area("system-prompt", sp1, key="sp1")
        pre_prompt1 = st.text_area("pre-prompt", pp1, key="pp1")
        question1 = st.text_area("question", qp1, key="qp1")

    with col2:
        st.title("the Teacher")
        model2 = st.selectbox("model", available_models, key="model2")
        system_prompt2 = st.text_area("system-prompt", sp2, key="sp2")
        pre_prompt2 = st.text_area("pre-prompt", pp2, key="pp2")
        # question2 = st.text_area("question", qp2, key="qp2")

    with col3:
        st.title("and the Kid")
        model3 = st.selectbox("model", available_models, key="model3")
        system_prompt3 = st.text_area("system-prompt", sp3, key="sp3")
        pre_prompt3 = st.text_area("pre-prompt", pp3, key="pp3")
        # question3 = st.text_area("question", qp3, key="qp3")

    with st.spinner("Thinking..."):
        answer1 = ask(model1, system_prompt1, pre_prompt1, question1)
        st.write(f":blue[Priest says:] {answer1}")

        qp2 = sanitize(answer1)

        answer2 = ask(model2, system_prompt2, pre_prompt2, qp2)
        st.write(f":blue[Teacher says:] {answer2}")


def sanitize(question):
    return re.sub(r"\([^)]*\)", "", question)


if __name__ == "__main__":
    main()
