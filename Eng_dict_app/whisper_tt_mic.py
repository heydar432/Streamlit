import sounddevice as sd
import scipy.io.wavfile as wav
import whisper

def record_and_transcribe(duration=5, sample_rate=44100, model_size="small", language="en"):
    # Record audio from the microphone
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    print("Recording finished")

    # Save the recording to a WAV file
    wav_file = "microphone_audio.wav"
    wav.write(wav_file, sample_rate, audio)

    # Load the Whisper model
    model = whisper.load_model(model_size, device="cpu")

    # Transcribe the recorded audio
    result = model.transcribe(wav_file, language=language)

    # Return the transcription text
    return result['text']

# Use the transcription in your main script
transcription = record_and_transcribe()

# You can now use 'transcription' wherever you need in your main script
print("Transcription:", transcription)

