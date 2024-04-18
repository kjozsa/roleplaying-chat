import re

import streamlit as st
from loguru import logger

# from .ollamachat import ask, models
from .togetherchat import ask, models

# from .transformerschat import ask, models

available_models = models()


class Scenario:
    def __init__(self, title, actors, pre_prompt, task):
        self.title = title
        self.actors = actors
        self.pre_prompt = pre_prompt
        self.task = task

    def __str__(self):
        return self.title


class Actor:
    actors = {}

    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt


def setup(scenario):
    st.markdown(  # top margin hack
        """
            <style>
                .appview-container .main .block-container {{
                    padding-top: {padding_top}rem;
                    padding-bottom: {padding_bottom}rem;
                    }}

            </style>""".format(
            padding_top=1, padding_bottom=1
        ),
        unsafe_allow_html=True,
    )
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
        temperature = st.slider("temperature", min_value=0.0, max_value=2.0, value=0.7, key="temperature")
        max_steps = st.slider("max-steps", min_value=1, max_value=10, value=6, key="max-steps")
    with col2:
        st.text_area("pre-prompt", scenario.pre_prompt)

    st.divider()
    st.header("Outcome")
    return model, max_steps, temperature


def main():
    st.set_page_config(layout="wide")
    scenarios = [
        Scenario(
            "Murder in the library", [
                Actor("Librarian", "You are the librarian. Today morning you found a dead body of an old lady laying on the floor. There is a visitor who just entered and a cleaning lady is standing in the corner."),
                Actor("Visitor",
                      "You are a visitor in the library. You wish to borrow an interesting book for two weeks to read on your upcoming vacation. There is a librarian who you can ask and a cleaning lady standing in the corner."),
                Actor("Cleaning lady", "You are the cleaning lady in the library. Today you came to work with a serious headache. There is a visitor and a librarian in the room."),
            ],
            "You are an actor in this roleplaying game. Your full response is said out loud and other people hear it. ",
            "Find out who committed the murder! You must find the clues by asking the two other people in the room."
        ),
        Scenario(
            "The Small Village scenario", [
                Actor("Priest", "You are the Priest. There are 3 people standing in a circle: the Priest (that's you), the Teacher and the Kid."),
                Actor("Teacher", "You are the Teacher. There are 3 people standing in a circle: the Priest, the Teacher (that's you) and the Kid."),
                Actor("Kid", "You are the Kid. There are 3 people standing in a circle: the Priest, the Teacher and the Kid (that's you).")
            ],
            "Answer questions as precisely as you can! If you want to ask anyone, always start your sentence with their role. Never start your sentence with your own name. Share your inner thoughts inside parentheses. SAY ONLY ONE SINGLE SENTENCE! Do not say 'sure, here is my response' or anything such)",
            "Priest, your task is to figure out their names and where they live. Do not ask directly, they must not realize what information you are after!"),

        Scenario(
            "The Number Guess Game", [
                Actor("Magician", "You are the Magician, and there is a Player standing next to you. Ask the Player about the secret number he thought of, guessing the number through questions."),
                Actor("Player", "You are the Player and there is a Magician next to you. Think of a secret number between 1 and 100. Answer received questions but do not tell the number directly."),
            ],
            "Always start your sentence with the name of the other person. Share your inner thoughts inside parentheses. NEVER start your sentence with your own name!",
            "Find out the secret number!"
        )
    ]

    scenario = st.selectbox("scenario", scenarios)
    model, max_steps, temperature = setup(scenario)
    main_loop(max_steps, model, scenario, temperature)


def main_loop(max_steps, model, scenario, temperature):
    questioner = None
    question = scenario.task
    actor = target(scenario, question, questioner)
    for step, _ in enumerate(range(max_steps), start=1):
        with st.spinner(f"({step}/{max_steps}) Asking {actor.name}..."):
            extended = f"{questioner} asks: {question}" if questioner else question
            answer = ask(model, actor.system_prompt, scenario.pre_prompt, extended, temperature=temperature)
            st.write(f":blue[{actor.name} says:] {answer}")
            question = sanitize(answer)
            questioner = actor.name
            actor = target(scenario, question, questioner)


def closest_to_start(long_string, substrings):
    logger.debug(f"looking for {substrings} in {long_string}")
    closest_index = len(long_string)
    closest_substring = None
    for substring in substrings:
        index = long_string.lower().find(substring.lower())
        if index != -1 and index < closest_index:
            closest_index = index
            closest_substring = substring
    return closest_substring


# noinspection PyTypeChecker
def target(scenario: Scenario, question, questioner) -> Actor:
    try:
        name = closest_to_start(question, [actor.name for actor in scenario.actors if actor.name != questioner])
        return [actor for actor in scenario.actors if actor.name == name][0]
    except IndexError:
        logger.warning(f"no actor found in question: {question}, trying to return the first actor")
        return scenario.actors[0]

    # try:
    #     role = re.split(r'\s|,|:', question.strip())[0].strip()
    #     logger.debug(f"finding actor with role: {role} in actors: {[actor.name for actor in scenario.actors]}")
    #     return [actor for actor in scenario.actors if actor.name == role][0]
    # except IndexError:
    #     logger.warning(f"no actor found in question: {question}, trying to return the first actor")
    #     return scenario.actors[0]


def sanitize(question):
    return re.sub(r"(\b\w+\s+(says|asks):\s*)?", "",
                  re.sub(r"(\b\w+\s+says:\s*)?\([^)]*\)", "", question)
                  )
