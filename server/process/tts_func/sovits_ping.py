import requests
import soundfile as sf
import sounddevice as sd
import yaml


with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)


def play_audio(path):
    data, samplerate = sf.read(path)
    sd.play(data, samplerate)
    sd.wait()


def sovits_gen(in_text, config, output_wav_pth="output.wav"):
    url = config["tts"]["providers"]["sovits"]["endpoint"]

    payload = {
        "text": in_text,
        "text_lang": config["tts"]["providers"]["sovits"]["text_lang"],
        "ref_audio_path": config["tts"]["providers"]["sovits"]["ref_audio_path"],
        "prompt_text": config["tts"]["providers"]["sovits"]["prompt_text"],
        "prompt_lang": config["tts"]["providers"]["sovits"]["prompt_lang"]
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()

        with open(output_wav_pth, "wb") as f:
            f.write(response.content)

        return output_wav_pth

    except Exception as e:
        print("Error in sovits_gen:", e)
        return None


if __name__ == "__main__":
    import time

    start = time.time()
    path = sovits_gen(
        "if you hear this, setup works",
        config,
        "output.wav"
    )
    print("Elapsed:", time.time() - start)
    print(path)