import whisper

# Load the Whisper model
model = whisper.load_model("small", device="cpu")

# Transcribe the audio file
result = model.transcribe(r"C:\Users\Heydar\Desktop\Data Science\My_projects\App for English words\voices/WhatsApp Ses 2024-08-27 saat 22.55.54_60edf367.waptt")

# Print the transcription
print(result['text'])
