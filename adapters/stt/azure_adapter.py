import os
import requests
from pathlib import Path
from datetime import datetime
from domain.entities import TranscriptResult
from domain.utils.lang_mapper import LanguageMapper


class AzureSTTAdapter:
    """
    Adaptador para el servicio Azure Speech-to-Text.

    Utiliza LanguageMapper para ajustar el idioma al formato
    esperado por Azure. Devuelve errores detallados en el campo 'raw'.
    """

    def __init__(self):
        """
        Inicializa el adaptador utilizando las variables de entorno
        AZURE_SPEECH_KEY y AZURE_REGION.
        """
        self.key = os.getenv("AZURE_SPEECH_KEY")
        self.region = os.getenv("AZURE_REGION")
        self.endpoint = (
            f"https://{self.region}.stt.speech.microsoft.com/"
            "speech/recognition/conversation/cognitiveservices/v1"
        )

        if not self.key or not self.region:
            raise ValueError(
                "Faltan variables de entorno: AZURE_SPEECH_KEY o AZURE_REGION."
            )

        print(f"[AzureSTTAdapter] Endpoint configurado: {self.endpoint}")

    def transcribe(self, audio_path: Path, language: str = "es-MX") -> TranscriptResult:
        """
        Transcribe un archivo de audio utilizando Azure Speech-to-Text.

        Si ocurre un error, incluye el mensaje detallado en el campo 'raw'.
        """
        mapped_lang = LanguageMapper.for_azure(language)

        try:
            with open(audio_path, "rb") as audio_file:
                response = requests.post(
                    f"{self.endpoint}?language={mapped_lang}",
                    headers={
                        "Ocp-Apim-Subscription-Key": self.key,
                        "Content-Type": "audio/wav",
                    },
                    data=audio_file,
                    timeout=30,
                )

            if response.status_code != 200:
                error_detail = (
                    f"Error de Azure STT ({response.status_code}): {response.text}"
                )
                print(f"[AzureSTTAdapter] {error_detail}")
                return TranscriptResult(
                    text="",
                    confidence=0.0,
                    language=mapped_lang,
                    timestamp=datetime.utcnow(),
                    provider="azure",
                    original_format="wav",
                    raw={"error": error_detail},
                )

            data = response.json()
            text = data.get("DisplayText", "").strip()
            status = data.get("RecognitionStatus", "Unknown")
            confidence = 0.9 if status == "Success" else 0.0

            return TranscriptResult(
                text=text,
                confidence=confidence,
                language=mapped_lang,
                timestamp=datetime.utcnow(),
                provider="azure",
                original_format="wav",
                raw=data,
            )

        except requests.exceptions.Timeout:
            error_detail = "Error: la solicitud a Azure STT excedió el tiempo límite."
            print(f"[AzureSTTAdapter] {error_detail}")
        except requests.exceptions.RequestException as e:
            error_detail = f"Error de conexión con Azure STT: {e}"
            print(f"[AzureSTTAdapter] {error_detail}")
        except Exception as e:
            error_detail = f"Error procesando la transcripción: {e}"
            print(f"[AzureSTTAdapter] {error_detail}")

        return TranscriptResult(
            text="",
            confidence=0.0,
            language=mapped_lang,
            timestamp=datetime.utcnow(),
            provider="azure",
            original_format="wav",
            raw={"error": error_detail},
        )
