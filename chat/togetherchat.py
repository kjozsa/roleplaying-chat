from loguru import logger
from openai import OpenAI
import os

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")

client = OpenAI(
    api_key=TOGETHER_API_KEY,
    base_url='https://api.together.xyz/v1',
)


def models():
    return [
        'teknium/OpenHermes-2p5-Mistral-7B',
        'meta-llama/Llama-2-13b-chat-hf',
        'meta-llama/Llama-2-70b-chat-hf',
        'Open-Orca/Mistral-7B-OpenOrca',
        'zero-one-ai/Yi-34B-Chat',
    ]


def ask(model, system_prompt, pre_prompt, question):
    messages = [
        {'role': 'system', 'content': f"{system_prompt} {pre_prompt}"},
        {'role': 'user', 'content': f"{question}"},
    ]
    logger.debug(f"<< {model} << {question}")

    chat_completion = client.chat.completions.create(messages=messages, model=model)
    response = chat_completion.choices[0]
    answer = response.message.content
    logger.debug(f">> {model} >> {answer}")
    return answer
