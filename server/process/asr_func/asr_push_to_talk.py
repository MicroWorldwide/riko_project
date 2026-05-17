import os
import sounddevice as sd
import soundfile as sf

def record_and_transcribe(model, output_file="recording.wav", samplerate=44100):
    if os.path.exists(output_file):
        os.remove(output_file)

    print("Press ENTER to start recording...")
    input()

    print("🔴 Recording... Press ENTER to stop")

    frames = []

    def callback(indata, frames_count, time, status):
        frames.append(indata.copy())

    stream = sd.InputStream(
        samplerate=samplerate,
        channels=1,
        dtype="float32",
        callback=callback
    )

    stream.start()
    input()  # stop trigger
    stream.stop()
    stream.close()

    audio = b"".join(frames)

    sf.write(output_file, audio, samplerate)

    print("🎯 Transcribing...")

    segments, _ = model.transcribe(output_file)

    transcription = " ".join(seg.text for seg in segments)

    print(f"Transcription: {transcription}")

    return transcription.strip()