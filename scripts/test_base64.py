import base64
import requests


def test_transcription_base64(file_path: str, provider: str = "teams", lang: str = "es"):
    """
    Envía un archivo de audio al endpoint /transcribe codificado en Base64.

    Argumentos:
        file_path: Ruta del archivo de audio a enviar.
        provider: Nombre del proveedor de origen (por defecto 'teams').
        lang: Idioma del audio (por defecto 'es').

    Retorna:
        dict: Respuesta JSON del servicio Tracky STT.
    """
    url = "http://127.0.0.1:8000/transcribe"

    try:
        with open(file_path, "rb") as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")

        payload = {
            "audio_base64": encoded_audio,
            "provider": provider,
            "lang": lang
        }

        print(f"[TestBase64] Enviando archivo {file_path} al servicio Tracky STT...")
        response = requests.post(url, data=payload, timeout=30)

        if response.status_code == 200:
            print("[TestBase64] Transcripción completada exitosamente.")
            return response.json()
        else:
            print(f"[TestBase64] Error ({response.status_code}): {response.text}")
            return {"error": response.text}

    except Exception as e:
        print(f"[TestBase64] Error ejecutando la prueba: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    """
    Ejecuta una prueba de transcripción a través de Base64.
    """
    result = test_transcription_base64("samples/teams.wav", provider="teams", lang="es-MX")
    print("\n[Resultado]\n", result)
