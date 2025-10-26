import json
import os

def load_config():
    config = {}
    config["AZURE_SPEECH_KEY"] = os.getenv("AZURE_SPEECH_KEY")
    config["AZURE_SPEECH_REGION"] = os.getenv("AZURE_SPEECH_REGION")
    config["AZURE_SPEECH_ENDPOINT"] = os.getenv("AZURE_SPEECH_ENDPOINT")

    if not all(config.values()):
        try:
            with open("config.local.json", "r", encoding="utf-8") as f:
                local_config = json.load(f)
                for key, value in local_config.items():
                    config[key] = config.get(key) or value
        except FileNotFoundError:
            raise FileNotFoundError("Archivo config.local.json no encontrado y no hay variables de entorno definidas.")
    
    return config
