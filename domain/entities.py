from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class AudioMeta:
    provider: str
    content_type: str
    lang: str = "es"

@dataclass
class TranscriptResult:
    text: str
    confidence: Optional[float]
    language: str
    timestamp: datetime
    provider: str
    original_format: str