import requests
import os

class AzureSTTAdapter:
    def __init__(self):
        self.key = os.getenv("AZURE_SPEECH_KEY")
        self.region = os.getenv("AZURE_REGION")
        self.endpoint = f"https://{self.region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
        print(f"Azure STT Adapter initialized with endpoint: {self.endpoint}")
        print(f"Using subscription key: {self.key}")
        print(f"Using region: {self.region}")

    def transcribe(self, audio_path, language="es-MX"):
        with open(audio_path, "rb") as audio_file:
            response = requests.post(
                f"{self.endpoint}?language={language}",
                headers={
                    "Ocp-Apim-Subscription-Key": self.key,
                    "Content-Type": "audio/wav",
                },
                data=audio_file,
            )

        if response.status_code != 200:
            raise Exception(f"Error de Azure STT ({response.status_code}): {response.text}")

        data = response.json()
        return data.get("DisplayText", "")
