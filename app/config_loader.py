import os
import json


def load_config() -> dict:
    """
    Carga la configuración del sistema Tracky STT.

    Prioriza las variables de entorno definidas en el sistema.
    Si alguna falta, intenta leer el archivo `config.local.json`
    ubicado en la raíz del proyecto.

    Retorna:
        dict: Diccionario con las variables de configuración requeridas.

    Lanza:
        FileNotFoundError: Si no existen las variables de entorno
                           ni el archivo local de configuración.
    """
    config = {
        "AZURE_SPEECH_KEY": os.getenv("AZURE_SPEECH_KEY"),
        "AZURE_SPEECH_REGION": os.getenv("AZURE_SPEECH_REGION"),
        "AZURE_SPEECH_ENDPOINT": os.getenv("AZURE_SPEECH_ENDPOINT"),
    }

    if all(config.values()):
        return config

    try:
        with open("config.local.json", "r", encoding="utf-8") as f:
            local_config = json.load(f)
            for key, value in local_config.items():
                config[key] = config.get(key) or value
    except FileNotFoundError:
        raise FileNotFoundError(
            "Archivo 'config.local.json' no encontrado "
            "y no existen variables de entorno definidas."
        )
    except json.JSONDecodeError:
        raise ValueError("El archivo 'config.local.json' contiene un formato JSON inválido.")

    return config
