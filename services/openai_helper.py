import openai, json, os
from config import OPENROUTER_KEY, SYSTEM_PROMPT

# puntiamo l'SDK a OpenRouter
openai.api_key  = OPENROUTER_KEY
openai.api_base = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-r1:free"

def parse_menu(text: str) -> dict:
    rsp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": text}
        ],
        response_format={"type": "json_object"}  # DeepSeek lo accetta
    )
    return json.loads(rsp.choices[0].message.content)
