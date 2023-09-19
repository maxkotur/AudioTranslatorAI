import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from googletrans import Translator
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
import textwrap
import tempfile
import os

# # Step 1: Extract audio from the MP4 file
input_video = "Gojko Kotur final v1.mp4"
output_audio = "input_audio.wav"
mp.VideoFileClip(input_video).audio.write_audiofile(output_audio, codec='pcm_s16le')

# Initialize the original_text variable
original_text = ""

# Step 2: Load the extracted audio
audio = AudioSegment.from_wav(output_audio)

# Function to split the audio into chunks
def split_audio(audio, chunk_size_ms):
    for i in range(0, len(audio), chunk_size_ms):
        yield audio[i:i+chunk_size_ms]

# Create the recognizer object outside of the loop
recognizer = sr.Recognizer()

# Create a temporary directory for audio chunks
temp_dir = tempfile.mkdtemp()

# Step 3: Process audio in chunks
chunk_size_ms = 60000  # Adjust the chunk size as needed (e.g., 60 seconds)
translated_text = ""

for i, audio_chunk in enumerate(split_audio(audio, chunk_size_ms)):
    # Save the audio chunk to a temporary WAV file
    temp_audio_file = os.path.join(temp_dir, f"temp_audio_{i}.wav")
    audio_chunk.export(temp_audio_file, format="wav")
    
    with sr.AudioFile(temp_audio_file) as source:
        try:
            # Recognize the speech in each chunk
            audio_data = recognizer.record(source)
            chunk_text = recognizer.recognize_google(audio_data, language='hr-HR')
            print(chunk_text)
            translated_text += chunk_text + ' '
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio in a chunk")
        except sr.RequestError as e:
            print(f"Error processing audio chunk: {e}")

# Step 4: Translate the concatenated text
# Initialize the translator
translator = Translator()

# Split the text into smaller chunks that end with complete sentences
chunk_size = 5000  # Adjust the chunk size as needed
chunks = textwrap.wrap(translated_text, chunk_size, break_long_words=False)

# Initialize the translated text
english_text = ""

# Translate each chunk and concatenate the results
for chunk in chunks:
    try:
        translated_result = translator.translate(chunk, src='hr', dest='en')
        if translated_result is not None:
            english_text += translated_result.text + " "
    except Exception as e:
        # Handle any exceptions that may occur during translation
        print(f"Translation error: {e}")

print(english_text)
# Step 5: Synthesize the translated text to speech
tts = gTTS(english_text, lang='en')
translated_audio = "translated_audio.mp3"
tts.save(translated_audio)

print("step 6")
# Step 6: Load the original video and the translated audio
input_video_clip = VideoFileClip(input_video)
translated_audio_clip = AudioFileClip(translated_audio)

print("step 7")
# Step 7: Set the translated audio to the video
video_with_translation = input_video_clip.set_audio(translated_audio_clip)

print("step 8")
# Step 8: Write the final video with translated audio
output_video = "output.mp4"
video_with_translation.write_videofile(output_video, codec='libx264')

# Step 9: Cleanup (remove temporary directory)
for temp_file in os.listdir(temp_dir):
    temp_file_path = os.path.join(temp_dir, temp_file)
    os.remove(temp_file_path)
os.rmdir(temp_dir)
