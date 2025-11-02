from google.cloud import speech
from google.oauth2 import service_account
from domain.ports import TranscriberPort
from domain.entities import TranscriptResult
from pathlib import Path
from datetime import datetime
import os


class GoogleSTTAdapter(TranscriberPort):
    """
    Adaptador agnóstico para Google Cloud Speech-to-Text.
    Utiliza el archivo de credenciales definido en la variable
    de entorno GOOGLE_APPLICATION_CREDENTIALS y devuelve un
    objeto TranscriptResult compatible con el dominio.
    """

    def __init__(self):
        creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not creds_path:
            raise ValueError("Falta la variable GOOGLE_APPLICATION_CREDENTIALS en el entorno.")
        credentials = service_account.Credentials.from_service_account_file(creds_path)
        self.client = speech.SpeechClient(credentials=credentials)

    def transcribe(self, wav_path: Path, language: str) -> TranscriptResult:
        with open(wav_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language,
            enable_automatic_punctuation=True
        )

        try:
            response = self.client.recognize(config=config, audio=audio)

            if not response.results:
                return TranscriptResult(
                    text="",
                    confidence=0.0,
                    language=language,
                    timestamp=datetime.utcnow(),
                    provider="google",
                    original_format=str(wav_path.suffix)
                )

            result = response.results[0].alternatives[0]
            return TranscriptResult(
                text=result.transcript.strip(),
                confidence=result.confidence,
                language=language,
                timestamp=datetime.utcnow(),
                provider="google",
                original_format=str(wav_path.suffix)
            )

        except Exception as e:
            return TranscriptResult(
                text="",
                confidence=0.0,
                language=language,
                timestamp=datetime.utcnow(),
                provider="google",
                original_format=str(wav_path.suffix),
                raw={"error": str(e)}
            )
        