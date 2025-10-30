from fastapi import FastAPI, Request
import requests
import json


app = FastAPI(title="Tracky Middleware Bot")

# URL del servicio STT interno
TRACKY_STT_URL = "http://127.0.0.1:8000/transcribe"


@app.post("/api/messages")
async def messages(request: Request):
    """
    Endpoint principal para recepción de mensajes desde plataformas externas.

    Diseñado originalmente para Microsoft Teams, este endpoint recibe
    mensajes con archivos de audio, los reenvía al servicio Tracky STT
    y devuelve una respuesta simple de confirmación.

    Argumentos:
        request: Cuerpo del mensaje recibido (payload JSON).

    Retorna:
        dict: Confirmación de recepción y, en caso de éxito,
              un resumen del resultado de transcripción.
    """
    try:
        body = await request.json()
        print(f"[MiddlewareBot] Mensaje recibido:\n{json.dumps(body, indent=2)}")

        # Extracción de archivos adjuntos de audio
        attachments = body.get("attachments", [])
        if not attachments:
            return {"status": "no_attachments", "detail": "No se adjuntó ningún archivo de audio."}

        results = []
        for att in attachments:
            content_type = att.get("contentType", "")
            if content_type.startswith("audio/"):
                audio_url = att.get("contentUrl")
                provider = body.get("source", "teams")
                print(f"[MiddlewareBot] Enviando audio a Tracky STT: {audio_url}")

                try:
                    response = requests.post(
                        TRACKY_STT_URL,
                        data={"audio_url": audio_url, "provider": provider, "lang": "es"},
                        timeout=30
                    )
                    if response.status_code == 200:
                        stt_result = response.json()
                        results.append(stt_result)
                        print(f"[MiddlewareBot] Transcripción recibida: {stt_result}")
                    else:
                        print(f"[MiddlewareBot] Error STT ({response.status_code}): {response.text}")

                except requests.exceptions.RequestException as e:
                    print(f"[MiddlewareBot] Error al comunicarse con STT: {e}")
                    results.append({"error": str(e)})

        return {
            "status": "received",
            "processed_audios": len(results),
            "results": results,
        }

    except Exception as e:
        print(f"[MiddlewareBot] Error procesando mensaje: {e}")
        return {"status": "error", "detail": str(e)}


@app.get("/health")
async def health():
    """
    Verificación de estado del middleware.

    Retorna:
        dict: Estado general y disponibilidad del middleware.
    """
    return {
        "status": "ok",
        "middleware": "Tracky Bot Bridge",
        "service": "Tracky STT",
    }
