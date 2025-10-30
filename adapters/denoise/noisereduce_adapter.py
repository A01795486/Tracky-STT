from pathlib import Path
import numpy as np
import librosa
import soundfile as sf
import noisereduce as nr
from scipy.signal import butter, lfilter
from domain.ports import NoiseReducerPort


class NoiseReduceAdapter(NoiseReducerPort):
    """
    Adaptador de reducción de ruido para Tracky STT.

    Aplica filtrado de banda y reducción de ruido mediante la librería
    `noisereduce`, estandarizando el audio a 16 kHz y canal mono para
    optimizar el desempeño de los motores STT.

    Métodos:
        reduce(wav_path):
            Procesa el archivo WAV aplicando filtros y reducción de ruido.
    """

    def __init__(self):
        self.sample_rate = 16000

    def _bandpass_filter(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Aplica un filtro pasa-banda entre 300 Hz y 3400 Hz."""
        nyq = 0.5 * sr
        low, high = 300 / nyq, 3400 / nyq
        b, a = butter(1, [low, high], btype="band")
        return lfilter(b, a, y)

    def _estimate_noise_level(self, y: np.ndarray) -> float:
        """Estima el nivel promedio de ruido en la señal de audio."""
        rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
        return float(np.percentile(rms, 20))

    def reduce(self, wav_path: Path) -> Path:
        """
        Reduce el ruido de un archivo WAV.

        Argumentos:
            wav_path: Ruta del archivo WAV a procesar.

        Retorna:
            Path: Ruta del archivo procesado (se sobrescribe el original).
        """
        try:
            y, sr = librosa.load(wav_path, sr=self.sample_rate, mono=True)
            y = self._bandpass_filter(y, sr)
            y_trimmed, _ = librosa.effects.trim(y, top_db=25)

            noise_level = self._estimate_noise_level(y_trimmed)
            print(f"[NoiseReduceAdapter] Nivel de ruido estimado: {noise_level:.4f}")

            prop = 0.9 if noise_level > 0.02 else 0.6
            y_clean = nr.reduce_noise(y=y_trimmed, sr=sr, prop_decrease=prop)

            if np.max(np.abs(y_clean)) > 0:
                y_clean = y_clean / np.max(np.abs(y_clean))

            sf.write(wav_path, y_clean, sr)
            print(f"[NoiseReduceAdapter] Archivo procesado correctamente: {wav_path.name}")
            return wav_path

        except Exception as e:
            print(f"[NoiseReduceAdapter] Error procesando {wav_path.name}: {e}")
            return wav_path
