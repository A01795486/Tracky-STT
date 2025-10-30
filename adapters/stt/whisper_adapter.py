from pathlib import Path
from datetime import datetime
import whisper
import numpy as np
import librosa
import re
import soundfile as sf
from domain.entities import TranscriptResult
from domain.utils.lang_mapper import LanguageMapper


class WhisperAdapter:
    """
    Adaptador para el motor Whisper de OpenAI.

    Realiza la transcripción de audio localmente.
    Usa LanguageMapper para normalizar el idioma
    y maneja errores de manera robusta.
    """

    def __init__(self, model_size: str = "medium"):
        """
        Inicializa el modelo Whisper con el tamaño indicado.
        """
        self.model = whisper.load_model(model_size)
        print(f"[WhisperAdapter] Modelo cargado: {model_size}")

    def transcribe(self, wav_path: Path, language: str) -> TranscriptResult:
        """
        Transcribe un archivo de audio usando Whisper.
        Si ocurre un error, devuelve un TranscriptResult con el detalle.
        """
        normalized_lang = LanguageMapper.for_whisper(language)

        try:
            y, sr = librosa.load(str(wav_path), sr=16000)
            if np.max(np.abs(y)) > 0:
                y = y / np.max(np.abs(y))
            sf.write(str(wav_path), y, sr)
        except Exception as e:
            error_detail = f"Error al preparar audio: {e}"
            print(f"[WhisperAdapter] {error_detail}")
            return TranscriptResult(
                text="",
                confidence=0.0,
                language=normalized_lang,
                timestamp=datetime.utcnow(),
                provider="whisper",
                original_format="wav",
                raw={"error": error_detail},
            )

        try:
            result = self.model.transcribe(
                str(wav_path),
                language=normalized_lang,
                temperature=0.0,
                beam_size=5,
                best_of=5,
                patience=1.0,
                condition_on_previous_text=False,
            )

            segments = result.get("segments", [])
            confidence = (
                float(np.mean([np.exp(seg.get("avg_logprob", -10)) for seg in segments]))
                if segments
                else 0.0
            )

            text = result.get("text", "").strip()
            text = re.sub(r"\s+", " ", text)
            text = text.replace("¿ ", "¿").replace(" ?", "?")

            return TranscriptResult(
                text=text,
                confidence=confidence,
                language=normalized_lang,
                timestamp=datetime.utcnow(),
                provider="whisper",
                original_format="wav",
                raw=result,
            )

        except ValueError as e:
            error_detail = f"Idioma no soportado por Whisper: {normalized_lang} ({e})"
            print(f"[WhisperAdapter] {error_detail}")
        except Exception as e:
            error_detail = f"Error durante la transcripción: {e}"
            print(f"[WhisperAdapter] {error_detail}")

        return TranscriptResult(
            text="",
            confidence=0.0,
            language=normalized_lang,
            timestamp=datetime.utcnow(),
            provider="whisper",
            original_format="wav",
            raw={"error": error_detail},
        )
