# AudioTranslatorAI
Audio translator to another language using AI

Given a video with no subtitles, translate it into another language using AI

The video used for this project is an interview in Serbo-croatian where we have
a real life personal story about Serbs during WW2.

I first implemented a dataset function which turns the audio into a dataset which
can be used for training. It could be a good reference if I wanted to created my own
serbo-croatian AI recognizer.

My main function uses **Whisper** from **HuggingFace** to first use the audio and translate it
into English. Since the audio file is 1 hour long, I separated it in chunks to properly
parse the data. The output can be found in translationAI.txt

My translator function uses google translate and the **speech_recognition** tools to first:
1. Get the mp4 file and transform it into a wav file
2. Load the extracted audio and create the recognizer object outside of the loop
3. Process the audio in chunks as it is too large in one go
4. Translate the concatenated text using google translate module which is also split into chunks
5. Synthesize the translated text to speech using **gTTS** (text to speech module)
6. Load the original video and the translated audio
7. Set the translated audio to the video
8. Write the final video with translated audio
9. Finally cleanup (remove temporary directory)

These 2 other text files are from the translator function and showcase the speech recognition
of Serbo-croatian and the translation of it into English. (speechrecog.txt and google_trans.txt)

Furthermore, we can find the translated audio in both mp3 and mp4 form.
