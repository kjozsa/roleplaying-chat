import streamlit as st
from ollama import chat

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
    response = chat(model=model, messages=[
        {
            'role': 'system',
            'content': f"{system_prompt}${pre_prompt}",
        },
        {
            'role': 'user',
            'content': f'${question}',
        },
    ])
    return response['message']['content']


def main():
    sp1 = """There are 3 people standing in a circle: the Priest (that's you), the Teacher and the Kid."""
    sp2 = """There are 3 people standing in a circle: the Priest, the Teacher (that's you) and the Kid."""
    sp3 = """There are 3 people standing in a circle: the Priest, the Teacher and the Kid (that's you)."""

    pp1 = pp2 = pp3 = "Ask the other two by always starting your sentence with their role. Always share your inner thoughts inside parentheses."
    qp1 = qp2 = qp3 = "Your task is to figure out their names and where they live. Do not ask directly, they must not realize what information you are after!"

    st.set_page_config(layout="wide")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.title("the Priest")
        model1 = st.selectbox(key="model1", label="model", options=available_models)
        system_prompt1 = st.text_area(key="sp1", label="system-prompt", value=sp1)
        pre_prompt1 = st.text_area(key="pp1", label="pre-prompt", value=pp1)
        question1 = st.text_area(key="q1", label="question", value=qp1)

    with col2:
        st.title("the Teacher")
        model2 = st.selectbox(key="model2", label="model", options=available_models)
        system_prompt2 = st.text_area(key="sp2", label="system-prompt", value=sp2)
        pre_prompt2 = st.text_area(key="pp2", label="pre-prompt", value=pp2)
        question2 = st.text_area(key="q2", label="question", value=qp2)

    with col3:
        st.title("the Kid")
        model3 = st.selectbox(key="model3", label="model", options=available_models)
        system_prompt3 = st.text_area(key="sp3", label="system-prompt", value=sp3)
        pre_prompt3 = st.text_area(key="pp3", label="pre-prompt", value=pp3)
        question3 = st.text_area(key="q3", label="question", value=qp3)

    with st.spinner("Thinking..."):
        answer1 = ask(model1, system_prompt1, pre_prompt1, question1)
        st.write(answer1)


if __name__ == "__main__":
    main()
