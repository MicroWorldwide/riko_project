import os
import queue
import sounddevice as sd
import soundfile as sf
import numpy as np
from faster_whisper import WhisperModel


def record_and_transcribe(
    model,
    output_file="recording.wav",
    samplerate=16000
):

    print("Press ENTER to start recording...")
    input()

    print("🔴 Recording... Press ENTER to stop")

    audio_queue = queue.Queue()
    recording = []

    def callback(indata, frames, time, status):
        if status:
            print(status)

        audio_queue.put(indata.copy())

    stream = sd.InputStream(
        samplerate=samplerate,
        channels=1,
        dtype='float32',
        callback=callback
    )

    stream.start()

    input()  # Wait for stop

    stream.stop()
    stream.close()

    print("⏹️ Processing audio...")

    while not audio_queue.empty():
        recording.append(audio_queue.get())

    if not recording:
        print("No audio recorded.")
        return ""

    audio = np.concatenate(recording, axis=0)

    # Save WAV
    sf.write(output_file, audio, samplerate)

    print("🎯 Transcribing...")

    segments, _ = model.transcribe(
        output_file,
        beam_size=5
    )

    transcription = " ".join(
        [segment.text for segment in segments]
    ).strip()

    if not transcription:
        print("No speech detected.")
        return ""

    print(f"Transcription: {transcription}")

    return transcription


if __name__ == "__main__":

    model = WhisperModel(
        "base.en",
        device="cpu",
        compute_type="float32"
    )

    result = record_and_transcribe(model)

    print(f"Got: '{result}'")