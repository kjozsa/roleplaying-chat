import re

import streamlit as st
from loguru import logger
from .togetherchat import ask, models

# from .transformerschat import ask, models

available_models = models()


class Actor:
    actors = {}

    def __init__(self, role, model, system_prompt, pre_prompt):
        self.role = role
        self.model = model
        self.system_prompt = system_prompt
        self.pre_prompt = pre_prompt
        Actor.actors[role] = self

    def __class_getitem__(cls, item):
        return cls.actors[item]


def setup(question):
    pp1 = pp2 = pp3 = "Answer questions as precisely as you can! If you want to ask anyone, always start your sentence with their role. Never start your sentence with your own name. Share your inner thoughts inside parentheses. SAY ONLY ONE SINGLE SENTENCE! Do not say 'sure, here is my response' or anything such)"
    priest = Actor("Priest", available_models[0], "You are the Priest. There are 3 people standing in a circle: the Priest (that's you), the Teacher and the Kid.", pp1)
    teacher = Actor("Teacher", available_models[0], "You are the Teacher. There are 3 people standing in a circle: the Priest, the Teacher (that's you) and the Kid.", pp2)
    kid = Actor("Kid", available_models[0], "You are the Kid. There are 3 people standing in a circle: the Priest, the Teacher and the Kid (that's you).", pp3)
    st.set_page_config(layout="wide")
    col1, col2, col3 = st.columns(3)
    for actor, col in [(priest, col1), (teacher, col2), (kid, col3)]:
        with col:
            role = actor.role
            st.title(role)
            actor.model = st.selectbox("model", available_models, key=f"{role}-model")
            actor.system_prompt = st.text_area("system-prompt", actor.system_prompt, key=f"{role}-sp")
            actor.pre_prompt = st.text_area("pre-prompt", actor.pre_prompt, key=f"{role}-pp")
    max_steps = st.slider("max-steps", min_value=1, max_value=10, value=6, key="max-steps")
    st.text_input("Priest's task", f"{question}")
    return question, max_steps


def main():
    question, max_steps = setup("Priest, your task is to figure out their names and where they live. Do not ask directly, they must not realize what information you are after!")
    questioner = None

    actor = target(sanitize(question))
    for step, _ in enumerate(range(max_steps), start=1):
        with st.spinner(f"({step}/{max_steps}) Asking {actor.role}..."):
            extended = f"{questioner} asks: {question}" if questioner else question
            answer = ask(actor.model, actor.system_prompt, actor.pre_prompt, extended)
            st.write(f":blue[{actor.role} says:] {answer}")
            question = sanitize(answer)
            questioner = actor.role
            actor = target(question)


# noinspection PyTypeChecker
def target(question) -> Actor:
    try:
        role = re.split(r'\s|,|:', question.strip())[0].strip()
        return Actor[role]
    except KeyError:
        logger.warning(f"no actor found in question: {question}, trying to return the first actor")
        return next(iter(Actor.actors.items()))[1]


def sanitize(question):
    return re.sub(r"(\b\w+\s+(says|asks):\s*)?", "",
                  re.sub(r"(\b\w+\s+says:\s*)?\([^)]*\)", "", question)
                  )
