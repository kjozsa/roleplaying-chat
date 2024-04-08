from loguru import logger
import ollama


def models():
    return sorted([x['model'] for x in ollama.list()['models']], key=lambda x: (not x.startswith("openhermes"), x))


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
    logger.debug(f"<< {model} << {question}")
    response = ollama.chat(model=model, messages=messages)
    answer = response['message']['content']
    logger.debug(f">> {model} >> {answer}")
    return answer
