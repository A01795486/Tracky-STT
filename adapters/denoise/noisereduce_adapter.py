from pathlib import Path
import numpy as np
import librosa
import soundfile as sf
import noisereduce as nr
from scipy.signal import butter, lfilter
from domain.ports import NoiseReducerPort


class NoiseReduceAdapter(NoiseReducerPort):
    def __init__(self):
        self.sample_rate = 16000

    def _bandpass_filter(self, y, sr):
        nyq = 0.5 * sr
        low, high = 300 / nyq, 3400 / nyq
        b, a = butter(1, [low, high], btype='band')
        return lfilter(b, a, y)

    def _estimate_noise_level(self, y):
        rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
        return float(np.percentile(rms, 20))

    def reduce(self, wav_path: Path) -> Path:
        try:
            y, sr = librosa.load(wav_path, sr=self.sample_rate, mono=True)
            y = self._bandpass_filter(y, sr)
            y_trimmed, _ = librosa.effects.trim(y, top_db=25)

            noise_level = self._estimate_noise_level(y_trimmed)
            print(f"[NoiseReduceAdapter] Nivel estimado de ruido: {noise_level:.4f}")

            if noise_level > 0.02:
                y_clean = nr.reduce_noise(y=y_trimmed, sr=sr, prop_decrease=0.9)
                print("[NoiseReduceAdapter] Reducción agresiva aplicada.")
            else:
                y_clean = nr.reduce_noise(y=y_trimmed, sr=sr, prop_decrease=0.6)
                print("[NoiseReduceAdapter] Reducción leve aplicada.")

            y_clean = np.clip(y_clean / np.max(np.abs(y_clean)), -1.0, 1.0)
            sf.write(wav_path, y_clean, sr)
            return wav_path

        except Exception as e:
            print(f"[NoiseReduceAdapter] Error procesando {wav_path.name}: {e}")
            return wav_path
