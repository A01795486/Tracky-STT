from domain.ports import TranscriberPort
from pathlib import Path

class GoogleSTTAdapter(TranscriberPort):
    def transcribe(self, wav_path: Path, language: str):
        return 'Transcripcin desde Google STT no implementada aun.'
