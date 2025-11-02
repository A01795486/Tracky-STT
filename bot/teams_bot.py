from fastapi import FastAPI, Request
import requests
import json

app = FastAPI(title="Tracky Middleware Bot")

TRACKY_STT_URL = "http://127.0.0.1:8000/transcribe"

@app.post("/api/messages")
async def messages(request: Request):
    body = await request.json()
    print(f"[MiddlewareBot] Mensaje recibido:\n{json.dumps(body, indent=2)}")

    attachments = body.get("attachments", [])
    for att in attachments:
        if att.get("contentType", "").startswith("audio/"):
            audio_url = att.get("contentUrl")
            print(f"[MiddlewareBot] Enviando audio a Tracky STT: {audio_url}")

            try:
                response = requests.post(
                    TRACKY_STT_URL,
                    data={
                        "audio_url": audio_url,
                        "provider": "teams",
                        "lang": "es-MX",
                        "stt_engine": "azure"
                    },
                    params={"mode": "full"}
                )
                print(f"[MiddlewareBot] Transcripción recibida: {response.json()}")
            except Exception as e:
                print(f"[MiddlewareBot] Error comunicando con Tracky STT: {e}")

    return {"status": "received"}
