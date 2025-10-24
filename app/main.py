# app/main.py
from fastapi import FastAPI, UploadFile, Form, HTTPException
from pathlib import Path
from dataclasses import asdict
from datetime import datetime
from domain.entities import AudioMeta
from domain.service import SttService
from adapters.decoder.factory import DecoderFactory
from adapters.denoise.noisereduce_adapter import NoiseReduceAdapter
from adapters.stt.stt_factory import STTFactory
from adapters.input.input_manager import InputManager


app = FastAPI(title="Tracky STT")

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = None,
    audio_url: str = Form(None),
    audio_base64: str = Form(None),
    provider: str = Form("unknown"),
    lang: str = Form("es"),
    #stt_engine: str = Form("whisper")  
):


    input_manager = InputManager(tmp_dir="./tmp")

    try:
        tmp = input_manager.process_input(file=file, audio_url=audio_url, audio_base64=audio_base64)
    except HTTPException as e:
        return {"error": e.detail}

    decoder = DecoderFactory.get(provider)
    denoiser = NoiseReduceAdapter()
    stt_adapter = STTFactory.get('whisper') 


    service = SttService(decoder, denoiser, stt_adapter)
    meta = AudioMeta(
        provider=provider,
        content_type=file.content_type if file else "url/base64",
        lang=lang
    )

    result = service.run(tmp, meta)
    return asdict(result)


@app.get("/health")
async def health():
    """Verifica que el servicio está corriendo."""
    return {"status": "ok", "service": "Tracky STT", "uptime": datetime.utcnow().isoformat()}
