from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form, HTTPException, Query
from datetime import datetime
from domain.entities import AudioMeta
from domain.service import SttService
from adapters.decoder.factory import DecoderFactory
from adapters.denoise.noisereduce_adapter import NoiseReduceAdapter
from adapters.stt.stt_factory import STTFactory
from adapters.input.input_manager import InputManager
from adapters.out.json_adapter import JsonResponseAdapter


load_dotenv()
app = FastAPI(title="Tracky STT")


@app.post("/transcribe")
async def transcribe(
    file: UploadFile = None,
    audio_url: str = Form(None),
    audio_base64: str = Form(None),
    provider: str = Form("unknown"),
    lang: str = Form("es-MX"),
    stt_engine: str = Form("whisper"),
    mode: str = Query("compact", description="Modo de salida: compact o full")
):
    """
    Endpoint principal de transcripción de audio.

    Permite enviar un archivo, URL o Base64 para su transcripción.
    Devuelve un resultado estructurado en modo compacto o completo.

    Argumentos:
        file: Archivo de audio cargado.
        audio_url: URL remota de un audio.
        audio_base64: Audio en cadena Base64.
        provider: Fuente del audio (WhatsApp, Teams, etc.).
        lang: Idioma para la transcripción (por defecto 'es-MX').
        stt_engine: Motor STT a usar ('azure', 'whisper', 'google').
        mode: Nivel de detalle del resultado ('compact' o 'full').

    Retorna:
        dict: Resultado serializado del proceso de transcripción.
    """
    try:
        tmp = InputManager("./tmp").process_input(file, audio_url, audio_base64)
    except HTTPException as e:
        return {"error": e.detail}

    decoder = DecoderFactory.get(
    provider=provider,
    file_path=tmp,
    mime_type=file.content_type if file else ""
    )

    denoiser = NoiseReduceAdapter()
    stt = STTFactory.get(stt_engine)
    service = SttService(decoder, denoiser, stt)

    meta = AudioMeta(
        provider=provider,
        content_type=file.content_type if file else "url/base64",
        lang=lang if "-" in lang else f"{lang}-MX"
    )

    result = service.run(tmp, meta)
    return JsonResponseAdapter.serialize(result, mode)


@app.get("/health")
async def health():
    """
    Verifica el estado de la API Tracky STT.

    Retorna:
        dict: Estado general del servicio.
    """
    return {
        "status": "ok",
        "service": "Tracky STT",
        "uptime": datetime.utcnow().isoformat()
    }
