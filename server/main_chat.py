from faster_whisper import WhisperModel
from process.asr_func.asr_push_to_talk import record_and_transcribe
from process.llm_funcs.llm_scr import llm_response
from process.tts_func.sovits_ping import sovits_gen, play_audio
from pathlib import Path
### transcribe audio 
import uuid
import soundfile as sf

print(' \n ========= Starting Chat... ================ \n')
whisper_model = WhisperModel("base.en", device="cpu", compute_type="int8")

while True:

    conversation_recording = Path("audio") / "conversation.wav"
    conversation_recording.parent.mkdir(parents=True, exist_ok=True)

    user_spoken_text = record_and_transcribe(whisper_model, conversation_recording)

    ### pass to LLM and get a LLM output.

    try:
        llm_output = llm_response(user_spoken_text)
        print(f"Riko: {llm_output}")
    except Exception as e:
        print(f"LLM error: {e}")
        continue

    tts_read_text = llm_output

    ### file organization 

    # 1. Generate a unique filename
    uid = uuid.uuid4().hex
    filename = f"output_{uid}.wav"
    output_wav_path = Path("audio") / filename
    output_wav_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate TTS audio
    gen_aud_path = sovits_gen(tts_read_text, output_wav_path)

    # Only play if generation succeeded
    if gen_aud_path and Path(gen_aud_path).exists():

        try:
            play_audio(gen_aud_path)

        except Exception as e:
            print(f"Audio playback error: {e}")

    else:
        print("TTS generation failed.")

    # # Example
    # duration = get_wav_duration(output_wav_path)

    # print("waiting for audio to finish...")
    # time.sleep(duration)