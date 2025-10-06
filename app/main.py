from pydub import AudioSegment
from fastapi import FastAPI, UploadFile, Form
from pathlib import Path
from domain.entities import AudioMeta
from domain.service import SttService
from adapters.decoder.ogg_opus import OggOpusDecoder
from adapters.denoise.noisereduce_adapter import NoiseReduceAdapter
from adapters.stt.whisper_adapter import WhisperAdapter
from datetime import datetime


app = FastAPI(title="Tracky STT")

@app.post("/transcribe")
async def transcribe(file: UploadFile, provider: str = Form("unknown"), lang: str = Form("es")):
    tmp = Path(file.filename)
    tmp.write_bytes(await file.read())

    decoder = OggOpusDecoder()
    denoiser = NoiseReduceAdapter()
    stt_engine = WhisperAdapter(model_size="base")

    service = SttService(decoder, denoiser, stt_engine)
    meta = AudioMeta(provider=provider, content_type=file.content_type, lang=lang)
    result = service.run(tmp, meta)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "provider": result.provider,
        "original_format": result.original_format,
        "language": result.language,
        "text": result.text
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
