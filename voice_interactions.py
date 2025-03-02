import openai
from dotenv import load_dotenv
import os
import time
import sounddevice as sd
from pynput import keyboard
import wave
import io
from pydub import AudioSegment, effects
from pydub.playback import play


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

# def adjust_pitch_and_speed(audio_segment, pitch_factor=4, speed=0.3, target_sample_rate=48000):
#     """Adjusts pitch and speed for a child-friendly effect, resetting to a standard sample rate."""
#     adjusted_segment = audio_segment._spawn(audio_segment.raw_data, overrides={
#         "frame_rate": int(audio_segment.frame_rate * pitch_factor * speed)
#     })
#     # Set final frame rate to a standard rate after adjustments
#     return adjusted_segment.set_frame_rate(target_sample_rate)

def stt_whisper():
    # This function uses OpenAI's whisper voice to text model to convert your voice input to text.
    record_audio()
    audio_file = open("user_response.wav", "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript.text

def record_audio(duration=None):
    CHUNK = 1024
    FORMAT = 'int16'
    CHANNELS = 1
    RATE = 10000
    WAVE_OUTPUT_FILENAME = "user_response.wav"

    frames = []
    stream = None
    is_recording = False
    recording_stopped = False

    def record_audio():
        nonlocal frames, stream
        frames = []

        stream = sd.InputStream(
            samplerate=RATE,
            channels=CHANNELS,
            dtype=FORMAT,
            blocksize=CHUNK,
            callback=callback
        )

        stream.start()

    def callback(indata, frame_count, time, status):
        nonlocal stream
        if is_recording:
            frames.append(indata.copy())

    def stop_recording():
        nonlocal frames, stream, recording_stopped

        stream.stop()
        stream.close()


        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        recording_stopped = True

    def on_key(key):
        nonlocal is_recording

        if key == keyboard.Key.up:
            if not is_recording:
                record_audio()
                is_recording = True
            else:
                stop_recording()
                is_recording = False

    listener = keyboard.Listener(on_press=on_key)
    listener.start()

    start_time = time.time()
    while listener.running:
        if recording_stopped:
            listener.stop()
        elif duration and (time.time() - start_time) > duration:
            listener.stop()
        time.sleep(0.01)



def tts_whisper(input, voice="nova"):
    response = client.audio.speech.create(
        model="tts-1",
        voice=f"{voice.lower()}",
        input=f"{input}",
    )
    audio_data = response.content
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
    play(audio_segment)