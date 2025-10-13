import whisper
import numpy as np
import librosa
import re
import soundfile as sf
from pathlib import Path
from domain.ports import TranscriberPort


class WhisperAdapter(TranscriberPort):
    
    def __init__(self, model_size: str = "medium"):
        self.model = whisper.load_model(model_size)
        print(f"[WhisperAdapter] Modelo cargado: {model_size}")

    def transcribe(self, wav_path: Path, language: str):

        try:
            y, sr = librosa.load(str(wav_path), sr=16000)
            if np.max(np.abs(y)) > 0:  
                y = y / np.max(np.abs(y))
            sf.write(str(wav_path), y, sr)
        except Exception as e:
            print(f"[WhisperAdapter] Error al normalizar audio: {e}")

        result = self.model.transcribe(
            str(wav_path),
            language=language,
            temperature=0.0,
            beam_size=5,
            best_of=5,
            patience=1.0,
            condition_on_previous_text=False
        )

        segments = result.get("segments", [])
        if segments:
            confidences = [np.exp(seg.get("avg_logprob", -10)) for seg in segments]
            confidence = float(np.mean(confidences))
        else:
            confidence = 0.0
        text = result.get("text", "").strip()
        text = re.sub(r"\s+", " ", text)
        text = text.replace("¿ ", "¿").replace(" ?", "?")

        print(f"[WhisperAdapter] Transcripción final: {text}")
        print(f"[WhisperAdapter] Confianza: {confidence:.3f}")
        return {"text": text, "confidence": confidence}
