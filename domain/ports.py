from typing import Protocol
from pathlib import Path
from domain.entities import AudioMeta, TranscriptResult

class AudioDecoderPort(Protocol):
    def to_wav_mono16k(self, src: Path) -> Path: ...

class NoiseReducerPort(Protocol):
    def reduce(self, wav_path: Path) -> Path: ...

class TranscriberPort(Protocol):
    def transcribe(self, wav_path: Path, language: str) -> TranscriptResult: ...