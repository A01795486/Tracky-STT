from pathlib import Path
from datetime import datetime
from domain.entities import AudioMeta, TranscriptResult
from domain.ports import AudioDecoderPort, NoiseReducerPort, TranscriberPort

class SttService:
    def __init__(self, decoder: AudioDecoderPort, denoiser: NoiseReducerPort, stt: TranscriberPort):
        self.decoder = decoder
        self.denoiser = denoiser
        self.stt = stt

    def run(self, file_path: Path, meta: AudioMeta) -> TranscriptResult:
        wav = self.decoder.to_wav_mono16k(file_path)
        wav_clean = self.denoiser.reduce(wav)
        result = self.stt.transcribe(wav_clean, language=meta.lang)
        return TranscriptResult(
            text=result.text,
            confidence=result.confidence,
            language=meta.lang,
            timestamp=datetime.utcnow(),
            provider=meta.provider,
            original_format=meta.content_type
        )

