import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from loguru import logger
import spaces


def models():
    return ["openhermes"]


def load():
    torch.set_default_device("cuda")
    model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
    return (model, tokenizer)


model, tokenizer = load()


def ask(_, system_prompt, pre_prompt, question):
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
    logger.debug(f"<< openhermes << {question}")
    inputs = tokenizer(question, return_tensors="pt", return_attention_mask=False)
    outputs = model.generate(**inputs, max_length=200)
    answer = tokenizer.batch_decode(outputs)[0]
    logger.debug(f">> openhermes >> {answer}")
    return answer
