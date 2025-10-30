from pathlib import Path
import soundfile as sf
import numpy as np
from librosa import resample
from domain.ports import AudioDecoderPort


class WavDecoder(AudioDecoderPort):
    """
    Decoder para archivos de audio en formato WAV.

    Asegura que cualquier archivo WAV sea convertido a
    formato estándar mono 16 kHz y normalizado, garantizando
    compatibilidad total con los motores de transcripción.

    Métodos:
        to_wav_mono16k(src):
            Convierte y normaliza un archivo WAV al formato estándar.
    """

    def to_wav_mono16k(self, src: Path) -> Path:
        """
        Convierte y normaliza un archivo WAV al formato estándar mono 16 kHz.

        Argumentos:
            src: Ruta del archivo WAV de entrada.

        Retorna:
            Path: Ruta del archivo convertido (.wav).
        """
        try:
            y, sr = sf.read(src)
            print(f"[WavDecoder] Archivo recibido: {src.name} | Frecuencia original: {sr} Hz")

            if y.ndim > 1:
                y = np.mean(y, axis=1)
                print("[WavDecoder] Convertido a mono.")

            if sr != 16000:
                y = resample(y, orig_sr=sr, target_sr=16000)
                sr = 16000
                print(f"[WavDecoder] Frecuencia ajustada a 16 kHz.")

            if np.max(np.abs(y)) > 0:
                y = y / np.max(np.abs(y))

            out_path = src.with_suffix(".wav")
            sf.write(out_path, y, sr)

            print(f"[WavDecoder] Archivo decodificado correctamente: {out_path.name}")
            return out_path

        except Exception as e:
            print(f"[WavDecoder] Error procesando {src.name}: {e}")
            return src
