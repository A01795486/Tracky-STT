from adapters.stt.whisper_adapter import WhisperAdapter
from adapters.stt.azure_adapter import AzureSTTAdapter
from adapters.stt.google_adapter import GoogleSTTAdapter

class STTFactory:
    @staticmethod
    def get(engine_name: str = "whisper"):
        engine_name = (engine_name or "whisper").strip().lower()

        if engine_name == "azure":
            print("Usando Azure Speech-to-Text.")
            return AzureSTTAdapter()
        elif engine_name == "google":
            print("Usando Google Cloud Speech.")
            return GoogleSTTAdapter()
        else:
            print("Usando Whisper.")
            return WhisperAdapter()


