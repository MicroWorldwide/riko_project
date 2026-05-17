import yaml
import json
import os
from openai import OpenAI

with open('config.yaml', 'r', encoding="utf-8") as f:
    char_config = yaml.safe_load(f)

client = OpenAI(
    api_key=char_config['openai']['api_key'],
    base_url=char_config['openai']['base_url']
)

HISTORY_FILE = char_config['history']['file']
MODEL = char_config['openai']['model']


def build_system_prompt(config):
    preset = config["character"]["active_preset"]
    path = config["character"]["presets"][preset]["system_prompt_file"]

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return [{"role": "system", "content": content}]


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def get_riko_response_no_tool(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.8,
    )
    return response.choices[0].message.content


def llm_response(user_input):
    messages = build_system_prompt(char_config) + load_history()

    messages.append({
        "role": "user",
        "content": user_input
    })

    assistant_reply = get_riko_response_no_tool(messages)

    messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    save_history(messages[len(build_system_prompt(char_config)):])

    return assistant_reply


if __name__ == "__main__":
    print("running main")