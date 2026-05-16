# Project Riko

Project Riko is a anime focused LLM project by Just Rayen. She listens, and remembers your conversations. It combines OpenAI’s GPT, Piper voice synthesis, and Faster-Whisper ASR into a fully configurable conversational pipeline.

**tested with python 3.10 Windows > 10 and Linux Ubuntu**

## ✨ Features

- 💬 **LLM-based dialogue** using OpenAI API (configurable system prompts) that connects to LM Studio
- 🧠 **Conversation memory** to keep context during interactions
- 🔊 **Voice generation** via Piper
- 🎧 **Speech recognition** using Faster-Whisper
- 📁 Clean YAML-based config for personality configuration

## ⚙️ Configuration

All prompts and parameters are stored in `config.yaml`.

```yaml
OPENAI_API_KEY: lm-studio
OPENAI_BASE_URL: "http://localhost:1234/v1"
model: "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF"
history_file: chat_history.json
presets:
  default:
    system_prompt: |
      You are a helpful assistant named Riko.
      You speak like a snarky anime girl.
      Always refer to the user as "senpai".
````

You can define personalities by modiying the config file.


## 🛠️ Setup

### Install Dependencies

```bash
pip install uv 
uv pip install -r extra-req.txt
uv pip install -r requirements.txt
```

**If you want to use GPU support for Faster whisper** Make sure you also have:

* CUDA & cuDNN installed correctly (for Faster-Whisper GPU support)
* `ffmpeg` installed (for audio processing)

## 🧪 Usage

### 1. Run the main script:

```bash
python main_chat.py
```

The flow:

1. Riko listens to your voice via microphone (push to talk)
2. Transcribes it with Faster-Whisper
3. Passes it to GPT (with history)
4. Generates a response
5. Synthesizes Riko's voice using Piper
6. Plays the output back to you

## 📌 TODO / Future Improvements

* [ ] GUI or web interface
* [ ] Live microphone input support
* [ ] Emotion or tone control in speech synthesis
* [ ] VRM model frontend

## 🧑‍🎤 Credits

* ASR via [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)
* Language model via [OpenAI GPT](https://platform.openai.com)

## 📜 License

MIT — feel free to clone, modify, and build your own waifu voice companion.
