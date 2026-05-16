import soundfile as sf
import sounddevice as sd
from pathlib import Path
import subprocess

VOICE_PATH = "models/piper/en_US-amy-medium.onnx"


def play_audio(path):
    try:
        data, samplerate = sf.read(path)
        sd.play(data, samplerate)
        sd.wait()
    except Exception as e:
        print(f"Playback error: {e}")


def piper_gen(in_text, output_wav_pth="output.wav"):
    """
    Reliable Piper TTS using CLI (most stable method)
    """

    output_wav_pth = str(Path(output_wav_pth))

    try:
        cmd = [
            "piper",
            "--model", VOICE_PATH,
            "--output_file", output_wav_pth
        ]

        subprocess.run(
            cmd,
            input=in_text.encode("utf-8"),
            check=True
        )

        return output_wav_pth

    except Exception as e:
        print(f"TTS error: {e}")
        return None


if __name__ == "__main__":

    test = piper_gen("Hello, this is a local TTS test.")
    if test:
        play_audio(test)