import whisper
import numpy as np
import librosa
import re
import soundfile as sf
from pathlib import Path
from domain.ports import TranscriberPort


class WhisperAdapter(TranscriberPort):
    def __init__(self, model_size: str = "medium"):
        # Carga del modelo Whisper
        self.model = whisper.load_model(model_size)
        print(f"[WhisperAdapter] Modelo cargadooooo: {model_size}")

    def transcribe(self, wav_path: Path, language: str):
        # --- Normalización previa del audio ---
        y, sr = librosa.load(str(wav_path), sr=16000)
        y = y / np.max(np.abs(y))  # normaliza amplitud (volumen)
        sf.write(str(wav_path), y, sr)  # guarda el audio normalizado

        # --- Transcripción ---
        result = self.model.transcribe(
            str(wav_path),
            language="es",
            temperature=0.0,
            beam_size=5,                # más precisión
            best_of=5,
            patience=1.0,
            condition_on_previous_text=False
        )

        # --- Postprocesamiento del texto ---
        text = result["text"]
        text = re.sub(r"\s+", " ", text.strip())  # limpia espacios
        text = text.replace("¿ ", "¿").replace(" ?", "?")  # corrige signos

        print(f"[WhisperAdapter] Transcripción final: {text}")
        return text
