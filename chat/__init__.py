import re

import streamlit as st
from loguru import logger
# from .togetherchat import ask, models
from .ollamachat import ask, models

# from .transformerschat import ask, models

available_models = models()


class Scenario:
    def __init__(self, title, actors, pre_prompt, task):
        self.title = title
        self.actors = actors
        self.pre_prompt = pre_prompt
        self.task = task


class Actor:
    actors = {}

    def __init__(self, name, model, system_prompt):
        self.name = name
        self.model = model
        self.system_prompt = system_prompt
        Actor.actors[name] = self

    def __class_getitem__(cls, item):
        return cls.actors[item]


def setup(scenario):
    st.set_page_config(layout="wide")
    st.title(scenario.title)
    columns = st.columns(len(scenario.actors))
    for actor, col in zip(scenario.actors, columns):
        with col:
            name = actor.name
            st.subheader(name)
            actor.system_prompt = st.text_area("system-prompt", actor.system_prompt, key=f"{name}-sp")

    st.text_input(f"{scenario.actors[0].name}'s task", f"{scenario.task}")
    st.subheader("Scenario setup")
    col1, col2 = st.columns([1, 4])
    with col1:
        model = st.selectbox("model", available_models)
        max_steps = st.slider("max-steps", min_value=1, max_value=10, value=6, key="max-steps")
    with col2:
        st.text_area("pre-prompt", scenario.pre_prompt)

    st.divider()
    st.header("Outcome")
    return model, max_steps


def main():
    scenario = Scenario("The Small Village scenario", [
        Actor("Priest", available_models[0], "You are the Priest. There are 3 people standing in a circle: the Priest (that's you), the Teacher and the Kid."),
        Actor("Teacher", available_models[0], "You are the Teacher. There are 3 people standing in a circle: the Priest, the Teacher (that's you) and the Kid."),
        Actor("Kid", available_models[0], "You are the Kid. There are 3 people standing in a circle: the Priest, the Teacher and the Kid (that's you).")
    ],
                        "Answer questions as precisely as you can! If you want to ask anyone, always start your sentence with their role. Never start your sentence with your own name. Share your inner thoughts inside parentheses. SAY ONLY ONE SINGLE SENTENCE! Do not say 'sure, here is my response' or anything such)",
                        "Priest, your task is to figure out their names and where they live. Do not ask directly, they must not realize what information you are after!")

    model, max_steps = setup(scenario)

    questioner = None
    question = scenario.task
    actor = target(question)
    for step, _ in enumerate(range(max_steps), start=1):
        with st.spinner(f"({step}/{max_steps}) Asking {actor.name}..."):
            extended = f"{questioner} asks: {question}" if questioner else question
            answer = ask(model, actor.system_prompt, scenario.pre_prompt, extended)
            st.write(f":blue[{actor.name} says:] {answer}")
            question = sanitize(answer)
            questioner = actor.name
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
