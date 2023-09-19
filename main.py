from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import librosa

# Load the Whisper processor and model
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")
forced_decoder_ids = processor.get_decoder_prompt_ids(language="bosnian", task="translate")

# Load and process your long audio file (ensure it's 16,000 Hz)
custom_audio_path = "output_audio.wav"
custom_audio, sr = librosa.load(custom_audio_path, sr=16000)  # Ensure 16,000 Hz sampling rate

# Split the long audio into smaller segments (e.g., 30-second chunks)
segment_duration = 30  # seconds
segment_length = sr * segment_duration

# Initialize a list to store transcriptions
transcriptions = []

# Process and transcribe each segment
for i in range(0, len(custom_audio), segment_length):
    segment = custom_audio[i:i + segment_length]
    input_features = processor(segment, sampling_rate=sr, return_tensors="pt").input_features

    # Generate token ids
    predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)

    # Decode token ids to text and append to the list
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    transcriptions.append(transcription)

# Concatenate transcriptions into a single text
full_transcription = " ".join(transcriptions)

# Print the full transcription
print(full_transcription)
