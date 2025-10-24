from domain.ports import TranscriberPort
from pathlib import Path

class AzureSTTAdapter(TranscriberPort):
    def transcribe(self, wav_path: Path, language: str):
        return 'Transcripción desde Azure STT no implementada aún.'
