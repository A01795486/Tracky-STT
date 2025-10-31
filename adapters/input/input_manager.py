from fastapi import UploadFile, HTTPException
from pathlib import Path
import base64
import requests
import mimetypes
import os


class InputManager:
    """
    Administrador de entradas de audio.

    Gestiona la recepción de archivos provenientes de distintas fuentes:
    - Subidas directas (UploadFile)
    - URLs remotas
    - Cadenas Base64

    Devuelve un objeto con la ruta del archivo temporal y el tipo MIME detectado.
    """

    def __init__(self, tmp_dir: str = "./tmp"):
        """
        Inicializa el directorio temporal donde se almacenan los audios procesados.
        """
        self.tmp_dir = Path(tmp_dir)
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def process_input(
        self,
        file: UploadFile = None,
        audio_url: str = None,
        audio_base64: str = None,
    ) -> dict:
        """
        Procesa el origen de entrada y guarda el archivo temporalmente.

        Retorna:
            dict: Contiene 'path' (Path del archivo) y 'mime_type' (str).
        """
        if file:
            tmp_path = self.tmp_dir / file.filename
            tmp_path.write_bytes(file.file.read())
            mime_type = file.content_type or mimetypes.guess_type(tmp_path.name)[0]
            return {"path": tmp_path, "mime_type": mime_type}

        elif audio_url:
            tmp_path = self.tmp_dir / "remote_audio"
            try:
                response = requests.get(audio_url)
                response.raise_for_status()
                ext = Path(audio_url).suffix or ".wav"
                tmp_path = tmp_path.with_suffix(ext)
                tmp_path.write_bytes(response.content)

                mime_type = (
                    response.headers.get("Content-Type")
                    or mimetypes.guess_type(tmp_path.name)[0]
                )
                return {"path": tmp_path, "mime_type": mime_type}

            except Exception as e:
                raise HTTPException(
                    status_code=400, detail=f"Error descargando audio remoto: {e}"
                )

        elif audio_base64:
            tmp_path = self.tmp_dir / "base64_audio.wav"
            try:
                audio_data = base64.b64decode(audio_base64)
                tmp_path.write_bytes(audio_data)
                mime_type = mimetypes.guess_type(tmp_path.name)[0] or "audio/wav"
                return {"path": tmp_path, "mime_type": mime_type}

            except Exception as e:
                raise HTTPException(
                    status_code=400, detail=f"Error procesando audio Base64: {e}"
                )

        raise HTTPException(
            status_code=400, detail="Debe enviarse un archivo, URL o Base64 de audio."
        )
