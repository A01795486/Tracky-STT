from fastapi import FastAPI, UploadFile, Form, HTTPException
from pathlib import Path
from dataclasses import asdict
from datetime import datetime
from domain.entities import AudioMeta
from domain.service import SttService
from adapters.decoder.factory import DecoderFactory
from adapters.denoise.noisereduce_adapter import NoiseReduceAdapter
from adapters.stt.whisper_adapter import WhisperAdapter
from adapters.input.input_manager import InputManager  

app = FastAPI(title="Tracky STT")

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = None,
    audio_url: str = Form(None),
    provider: str = Form("unknown"),
    lang: str = Form("es")
):

    input_manager = InputManager(tmp_dir="./tmp")
    try:
        tmp = input_manager.process_input(file=file, audio_url=audio_url)
    except HTTPException as e:
        return {"error": e.detail}

    decoder = DecoderFactory.get(provider)
    denoiser = NoiseReduceAdapter()
    stt_engine = WhisperAdapter()

    service = SttService(decoder, denoiser, stt_engine)
    meta = AudioMeta(
        provider=provider,
        content_type=file.content_type if file else "url/audio",
        lang=lang
    )
    
    result = service.run(tmp, meta)
    return asdict(result)

@app.get("/health")
async def health():
    return {"status": "ok"}
