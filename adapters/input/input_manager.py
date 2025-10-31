from fastapi import UploadFile, HTTPException
from pathlib import Path
import base64
import requests
import mimetypes
import re


class InputManager:
    """
    Administra la entrada de audio desde diferentes fuentes:
    - Archivo (UploadFile)
    - URL remota
    - Cadena Base64
    """

    def __init__(self, tmp_dir: str = "./tmp"):
        self.tmp_dir = Path(tmp_dir)
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, name: str) -> str:
        """Elimina caracteres no válidos para nombres de archivo en Windows y Linux."""
        return re.sub(r'[\\/*?:"<>|]', "_", name)

    def process_input(self, file: UploadFile = None, audio_url: str = None, audio_base64: str = None) -> dict:
        if file:
            tmp_path = self.tmp_dir / self._sanitize_filename(file.filename)
            tmp_path.write_bytes(file.file.read())
            mime_type = file.content_type or mimetypes.guess_type(tmp_path.name)[0]
            return {"path": tmp_path, "mime_type": mime_type}

        elif audio_url:
            try:
                # 1️⃣ Cortar parámetros tipo ?t=xxxxx
                clean_url = audio_url.split("?")[0]
                # 2️⃣ Obtener nombre y extensión seguros
                name = Path(clean_url).name
                safe_name = self._sanitize_filename(name or "remote_audio.ogg")
                tmp_path = self.tmp_dir / safe_name

                response = requests.get(audio_url)
                response.raise_for_status()
                tmp_path.write_bytes(response.content)

                mime_type = (
                    response.headers.get("Content-Type")
                    or mimetypes.guess_type(tmp_path.name)[0]
                    or "audio/ogg"
                )

                return {"path": tmp_path, "mime_type": mime_type}

            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error descargando audio remoto: {e}")

        elif audio_base64:
            tmp_path = self.tmp_dir / "base64_audio.wav"
            try:
                audio_data = base64.b64decode(audio_base64)
                tmp_path.write_bytes(audio_data)
                mime_type = mimetypes.guess_type(tmp_path.name)[0] or "audio/wav"
                return {"path": tmp_path, "mime_type": mime_type}
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error procesando audio Base64: {e}")

        raise HTTPException(status_code=400, detail="Debe enviarse un archivo, URL o Base64 de audio.")
