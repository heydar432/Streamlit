import whisper

# Load the Whisper model
model = whisper.load_model("small")

voice_path = r"/home/heydar/Desktop/Data_Science/Minapy/transcribe using Whisper/Whisper_detailed_tests/recordings_for_comparison using app_2_for_comparison.py and app_2_config_for_comparison.yaml/full_audio_20240808_155642.wav"
# Transcribe the audio file
result = model.transcribe(voice_path, language = 'en')

# Print the transcription
print(result['text'])

