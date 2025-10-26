from domain.ports import TranscriberPort
from app.config_loader import load_config
import requests

class AzureSTTAdapter(TranscriberPort):
    def __init__(self):
        cfg = load_config()
        self.key = cfg["AZURE_SPEECH_KEY"]
        self.region = cfg["AZURE_SPEECH_REGION"]
        self.endpoint = cfg["AZURE_SPEECH_ENDPOINT"]
        if not self.key or not self.region:
            raise ValueError("Faltan las credenciales de Azure Speech.")

    def transcribe(self, wav_path, language="es-MX"):
        url = f"{self.endpoint}speech/recognition/conversation/cognitiveservices/v1"
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "audio/wav",
            "Accept": "application/json"
        }

        with open(wav_path, "rb") as f:
            audio_data = f.read()

        params = {"language": language}
        response = requests.post(url, headers=headers, params=params, data=audio_data)

        if response.status_code != 200:
            raise Exception(f"Error de Azure STT: {response.text}")

        data = response.json()
        return {"text": data.get("DisplayText", ""), "confidence": 1.0}
