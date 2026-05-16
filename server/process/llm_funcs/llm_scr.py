import yaml
import gradio as gr
import json
import os
from openai import OpenAI

with open('character_config.yaml', 'r') as f:
    char_config = yaml.safe_load(f)

client = OpenAI(
    api_key=char_config['OPENAI_API_KEY'],
    base_url=char_config['OPENAI_BASE_URL']
)

# Constants
HISTORY_FILE = char_config['history_file']
MODEL = char_config['model']

SYSTEM_PROMPT = [
    {
        "role": "system",
        "content": char_config['presets']['default']['system_prompt']
    }
]

# Load/save chat history
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return SYSTEM_PROMPT.copy()

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def get_riko_response_no_tool(messages):

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.8,
    )

    assistant_reply = response.choices[0].message.content

    return assistant_reply

def llm_response(user_input):

    messages = load_history()

    # Append user message
    messages.append({
        "role": "user",
        "content": user_input
    })

    # Get assistant response
    assistant_reply = get_riko_response_no_tool(messages)

    # Save assistant response to history
    messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    save_history(messages)

    return assistant_reply

if __name__ == "__main__":
    print('running main')