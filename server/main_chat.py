from faster_whisper import WhisperModel
from process.asr_func.asr_push_to_talk import record_and_transcribe
from process.llm_funcs.llm_scr import llm_response
from process.tts_func.piper_ping import piper_gen, play_audio
from pathlib import Path
import uuid
import soundfile as sf


def get_wav_duration(path):
    with sf.SoundFile(path) as f:
        return len(f) / f.samplerate


print("\n ========= Starting Chat... ================ \n")

whisper_model = WhisperModel(
    "base.en",
    device="cpu",
    compute_type="float32"
)

while True:

    # -------------------------
    # AUDIO INPUT (ASR)
    # -------------------------
    conversation_recording = Path("audio") / "conversation.wav"
    conversation_recording.parent.mkdir(parents=True, exist_ok=True)

    user_spoken_text = record_and_transcribe(
        whisper_model,
        conversation_recording
    )

    if not user_spoken_text.strip():
        print("No speech detected.")
        continue

    print(f"You: {user_spoken_text}")

    # -------------------------
    # LLM RESPONSE
    # -------------------------
    try:
        llm_output = llm_response(user_spoken_text)
        print(f"Riko: {llm_output}")

    except Exception as e:
        print(f"LLM error: {e}")
        continue

    # -------------------------
    # TTS INPUT
    # -------------------------
    tts_text = llm_output.strip()

    if not tts_text:
        print("Empty LLM response, skipping TTS.")
        continue

    # -------------------------
    # TTS GENERATION
    # -------------------------
    uid = uuid.uuid4().hex
    output_wav_path = Path("audio") / f"output_{uid}.wav"
    output_wav_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        gen_aud_path = piper_gen(tts_text, output_wav_path)

    except Exception as e:
        print(f"TTS error: {e}")
        continue

    # -------------------------
    # AUDIO PLAYBACK
    # -------------------------
    if gen_aud_path and Path(gen_aud_path).exists():

        try:
            play_audio(gen_aud_path)

        except Exception as e:
            print(f"Audio playback error: {e}")

    else:
        print("TTS generation failed.")