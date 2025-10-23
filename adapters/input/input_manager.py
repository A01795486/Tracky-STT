import requests
from pathlib import Path
from fastapi import UploadFile, HTTPException
import mimetypes
import uuid

class InputManager:


    def __init__(self, tmp_dir: str = "./tmp"):
        self.tmp_dir = Path(tmp_dir)
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def process_input(self, file: UploadFile = None, audio_url: str = None) -> Path:


        if not file and not audio_url:
            raise HTTPException(status_code=400, detail="se debee enviar un archivo o una URL de audio.")

        if file:
     
            tmp_file = self.tmp_dir / f"{uuid.uuid4()}_{file.filename}"
            tmp_file.write_bytes(file.file.read())
            print(f"[InputManager] Archivo recibido y guardado temporalmente: {tmp_file.name}")
            return tmp_file

        if audio_url:
      
            try:
                response = requests.get(audio_url, timeout=15)
                response.raise_for_status()

       
                content_type = response.headers.get("Content-Type", "audio/ogg")
                ext = mimetypes.guess_extension(content_type) or ".ogg"

                tmp_file = self.tmp_dir / f"{uuid.uuid4()}{ext}"
                tmp_file.write_bytes(response.content)
                print(f"[InputManager] Archivo descargado desde URL: {tmp_file.name}")
                return tmp_file

            except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=400, detail=f"No se pudo descargar el audio desde la URL: {str(e)}")
