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
            'content': system_prompt,
        },
        {
            'role': 'user',
            'content': f'${pre_prompt}${question}',
        },
    ])
    return response['message']['content']


def main():
    sp = """There are 3 people standing in a circle: you (the Priest), a Teacher and a Kid. You can ask the other two by starting your sentence with their role. 
    You act only as the Priest and wait for the others to answer. Always share your inner thoughts inside parentheses."""
    pp = "Your task is to figure out their names and where they live. Do not reveal your intentions, they must not realize what information you need!"
    qp = "Talk to the other two people, accomplishing your task."

    st.set_page_config(layout="wide")
    st.title("role playing experiments")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.title("the Teacher")
        model = st.selectbox("model", available_models)
        system_prompt = st.text_area("system-prompt", value=sp)
        pre_prompt = st.text_area("pre-prompt", value=pp)
        question = st.text_area("question", value=qp)

        with st.spinner("Thinking..."):
            answer = ask(model, system_prompt, pre_prompt, question)
            st.write(answer)


if __name__ == "__main__":
    main()
