import base64
import requests

file_path = "whatsapp.wav"

url = "http://127.0.0.1:8080/transcribe"

with open(file_path, "rb") as audio_file:
    encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")

payload = {
    "audio_base64": encoded_audio,
    "provider": "teams",
    "lang": "es"
}

print("probando que si llegue aquí")
response = requests.post(url, data=payload)

print("\nresponse:")
print(response.json())
