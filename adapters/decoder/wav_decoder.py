from pathlib import Path
import soundfile as sf
import numpy as np
from domain.ports import AudioDecoderPort


class WavDecoder(AudioDecoderPort):

    def to_wav_mono16k(self, src: Path) -> Path:
        try:
            y, sr = sf.read(src)
            print(f"WavDecoder rchivo recibido: {src.name} | Frecuencia: {sr} Hz")

            if y.ndim > 1:
                y = np.mean(y, axis=1)
                print("WavDecoder Archivo convertido a mono.")

            if sr != 16000:
                from librosa import resample
                y = resample(y, orig_sr=sr, target_sr=16000)
                sr = 16000
                print(f"WavDecoder Resampleado de {sr} Hz a 16 kHz.")

            y = y / np.max(np.abs(y)) if np.max(np.abs(y)) > 0 else y

            out_path = src.with_suffix(".wav")
            sf.write(out_path, y, sr)
            print(f"WavDecoder Archivo decodificado: {out_path.name}")
            return out_path

        except Exception as e:
            print(f"WavDecoder Error procesando {src.name}: {e}")
            return src
