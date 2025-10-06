from pathlib import Path
import librosa, soundfile as sf, noisereduce as nr
from domain.ports import NoiseReducerPort

class NoiseReduceAdapter(NoiseReducerPort):
    def reduce(self, wav_path: Path) -> Path:
        y, sr = librosa.load(wav_path, sr=16000, mono=True)
        y_clean = nr.reduce_noise(y=y, sr=sr)
        sf.write(wav_path, y_clean, sr)
        return wav_path
