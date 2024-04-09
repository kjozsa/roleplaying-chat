from ctransformers import AutoModelForCausalLM, AutoTokenizer
from loguru import logger
import os


def models():
    return ["mistral-7b-openorca.Q5_K_M.gguf"]


def load():
    # model = AutoModelForCausalLM.from_pretrained("TheBloke/OpenHermes-2.5-Mistral-7B-GGUF", model_file="openhermes-2.5-mistral-7b.Q4_K_M.gguf", model_type="mistral", gpu_layers=0, hf=True)

    model = AutoModelForCausalLM.from_pretrained(
        model_path_or_repo_id="TheBloke/Mistral-7B-OpenOrca-GGUF",
        model_file="mistral-7b-openorca.Q5_K_M.gguf",
        model_type="mistral",
        hf=True,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1.2,
        context_length=32768,
        max_new_tokens=2048,
        threads=os.cpu_count(),
        stream=True,
        gpu_layers=0
    )

    tokenizer = AutoTokenizer.from_pretrained(model)
    return (model, tokenizer)


model, tokenizer = load()


def ask(_, system_prompt, pre_prompt, question):
    messages = [
        {'role': 'system', 'content': f"{system_prompt} {pre_prompt}", },
        {'role': 'user', 'content': f"{question}", },
    ]
    logger.debug(f"<< transformers << {messages}")
    inputs = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    # inputs = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)

    outputs = model.generate(inputs, max_length=200)
    answer = tokenizer.batch_decode(outputs)[0]
    logger.debug(f">> transformers >> {answer}")
    return answer
