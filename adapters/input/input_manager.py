from fastapi import UploadFile, HTTPException
from pathlib import Path
import base64, requests
import os

class InputManager:
    def __init__(self, tmp_dir: str = "./tmp"):
        self.tmp_dir = Path(tmp_dir)
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def process_input(self, file: UploadFile = None, audio_url: str = None, audio_base64: str = None) -> Path:
 
        if file:
            tmp = self.tmp_dir / file.filename
            tmp.write_bytes(file.file.read())
            return tmp

        elif audio_url:
            tmp = self.tmp_dir / "remote_audio.wav"
            try:
                r = requests.get(audio_url)
                r.raise_for_status()
                tmp.write_bytes(r.content)
                return tmp
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error descargando audio remoto: {e}")

        elif audio_base64:
            tmp = self.tmp_dir / "base64_audio.wav"
            try:
                audio_data = base64.b64decode(audio_base64)
                tmp.write_bytes(audio_data)
                return tmp
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error procesando audio Base64: {e}")

        else:
            raise HTTPException(status_code=400, detail="Debe enviarse un archivo, URL o Base64 de audio.")
