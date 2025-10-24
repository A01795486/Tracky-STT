import base64
from pathlib import Path
import uuid

class InputAdapter:


    @staticmethod
    def get_audio_input(audio_base64: str) -> Path:
        if not audio_base64:
            raise ValueError("No se proporcionó audio en formato Base64.")
        
        try:
            audio_data = base64.b64decode(audio_base64)
            tmp_file = Path(f"./tmp/{uuid.uuid4()}_base64.wav")
            tmp_file.parent.mkdir(parents=True, exist_ok=True)
            tmp_file.write_bytes(audio_data)
            print(f"[InputAdapter] Audio decodificado desde Base64: {tmp_file.name}")
            return tmp_file
        
        except Exception as e:
            raise ValueError(f"Error procesando audio Base64: {e}")
