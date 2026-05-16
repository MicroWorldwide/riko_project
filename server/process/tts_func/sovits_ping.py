import soundfile as sf
import sounddevice as sd
import piper.voice
from pathlib import Path

# Load model once (important for speed)
VOICE_PATH = "models/piper/en_US-lessac-medium.onnx"

voice = piper.voice.PiperVoice.load(VOICE_PATH)


def play_audio(path):
    try:
        data, samplerate = sf.read(path)
        sd.play(data, samplerate)
        sd.wait()
    except Exception as e:
        print(f"Playback error: {e}")


def sovits_gen(in_text, output_wav_pth="output.wav"):
    """
    Drop-in replacement for GPT-SoVITS generator
    Now uses local Piper TTS
    """

    try:
        output_wav_pth = Path(output_wav_pth)

        with open(output_wav_pth, "wb") as f:
            voice.synthesize(in_text, f)

        return str(output_wav_pth)

    except Exception as e:
        print(f"TTS error: {e}")
        return None


if __name__ == "__main__":

    test = sovits_gen("Hello, this is a local TTS test.")
    if test:
        play_audio(test)