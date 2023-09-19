from pydub import AudioSegment
import numpy as np
import librosa
import soundfile as sf
import tempfile
from datasets import IterableDataset

# Create an IterableDataset
class AudioDataset(IterableDataset):
    def __init__(self, wav_paths):
        self.wav_paths = wav_paths

    def __iter__(self):
        for path in self.wav_paths:
            y, sr = librosa.load(path)
            yield {"audio": y, "sampling_rate": sr}

def get_dataset():
    # Load wav file
    audio = AudioSegment.from_mp3("output_audio.wav")

    # Convert the audio segment to a numpy.ndarray
    audio_array = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768

    # Save the numpy array as a temporary WAV file
    temp_wav_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    sf.write(temp_wav_path, audio_array, int(audio.frame_rate))
    
    # Create an instance of IterableDataset
    dataset = AudioDataset([temp_wav_path])
    
    return dataset