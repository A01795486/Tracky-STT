import whisper
from pathlib import Path
from domain.ports import TranscriberPort
from domain.entities import TranscriptResult

class WhisperAdapter(TranscriberPort):
    def __init__(self, model_size: str = "base"):
        self.model = whisper.load_model(model_size)

    def transcribe(self, wav_path: Path, language: str) -> TranscriptResult:
        r = self.model.transcribe(str(wav_path), language=language)
        return TranscriptResult(
            text=r["text"].strip(),
            confidence=None,
            language=language,
            timestamp=None,
            provider="",
            original_format=""
        )
