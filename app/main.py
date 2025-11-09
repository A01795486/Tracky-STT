from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form, HTTPException, Query
from dataclasses import asdict
from datetime import datetime
from domain.entities import AudioMeta
from domain.service import SttService
from adapters.decoder.factory import DecoderFactory
from adapters.denoise.noisereduce_adapter import NoiseReduceAdapter
from adapters.stt.stt_factory import STTFactory
from adapters.input.input_manager import InputManager
from adapters.out.json_adapter import JsonResponseAdapter

load_dotenv()
SAVE_INPUT_FILES = False
app = FastAPI(title="Tracky STT API")


@app.post("/transcribe")
async def transcribe(
    file: UploadFile = None,
    audio_url: str = Form(None),
    audio_base64: str = Form(None),
    provider: str = Form("unknown"),
    lang: str = Form("es-MX"),
    stt_engine: str = Form("google"),
    mode: str = Query("compact", description="Modo de salida: compact o full")
):
    """
    Endpoint principal de transcripción.
    Recibe audio desde múltiples fuentes (archivo, URL o Base64),
    detecta automáticamente el formato y devuelve el resultado normalizado.
    """
    input_manager = InputManager(tmp_dir="./tmp", save_files=SAVE_INPUT_FILES)

    try:
        input_data = input_manager.process_input(
            file=file, audio_url=audio_url, audio_base64=audio_base64
        )
    except HTTPException as e:
        return {"error": e.detail}

    decoder = DecoderFactory.get(
        provider=provider,
        file_path=input_data["path"],
        mime_type=input_data["mime_type"]
    )

    denoiser = NoiseReduceAdapter()
    stt_adapter = STTFactory.get(stt_engine)

    service = SttService(decoder, denoiser, stt_adapter)
    meta = AudioMeta(
        provider=provider,
        content_type=input_data["mime_type"],
        lang=lang
    )

    result = service.run(input_data["path"], meta)
    input_manager.cleanup(input_data["path"])
    return JsonResponseAdapter.serialize(result, mode=mode)


@app.get("/health")
async def health():
    """
    Endpoint de verificación de estado del servicio.
    """
    return {
        "status": "ok",
        "service": "Tracky STT",
        "uptime": datetime.utcnow().isoformat()
    }


