from fastapi import UploadFile, HTTPException
from pathlib import Path
import base64
import requests
import mimetypes
import re
import tempfile
import uuid


class InputManager:
    """
    Administra la entrada de audio desde diferentes fuentes:
    - Archivo (UploadFile)
    - URL remota
    - Cadena Base64
    """

    def __init__(self, tmp_dir: str = "./tmp", save_files: bool = False):
        self.tmp_dir = Path(tmp_dir)
        self.save_files = save_files 
        if self.save_files:
            self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def _create_temp_path(self, suffix=".wav") -> Path:
        """Crea un archivo temporal o persistente según la configuración."""
        if self.save_files:
            return self.tmp_dir / f"temp_{uuid.uuid4()}{suffix}"
        else:
            import tempfile
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            return Path(tmp.name)

    def _sanitize_filename(self, name: str) -> str:
        """Elimina caracteres no válidos para nombres de archivo en Windows y Linux."""
        return re.sub(r'[\\/*?:"<>|]', "_", name)

    def process_input(self, file: UploadFile = None, audio_url: str = None, audio_base64: str = None) -> dict:
        if file:
            tmp_path = self._create_temp_path(Path(file.filename).suffix)
            tmp_path.write_bytes(file.file.read())
            mime_type = file.content_type or mimetypes.guess_type(tmp_path.name)[0]
            return {"path": tmp_path, "mime_type": mime_type}

        elif audio_url:
            try:
                
                clean_url = audio_url.split("?")[0]
         
                name = Path(clean_url).name
                safe_name = self._sanitize_filename(name or "remote_audio.ogg")
                tmp_path = self._create_temp_path(Path(safe_name).suffix)

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
            tmp_path = self._create_temp_path(".wav")
            try:
                audio_data = base64.b64decode(audio_base64)
                tmp_path.write_bytes(audio_data)
                mime_type = mimetypes.guess_type(tmp_path.name)[0] or "audio/wav"
                return {"path": tmp_path, "mime_type": mime_type}
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error procesando audio Base64: {e}")

        raise HTTPException(status_code=400, detail="Debe enviarse un archivo, URL o Base64 de audio.")
    
    def cleanup(self, path: Path):
        """Elimina archivos temporales si no deben conservarse."""
        if not self.save_files and path.exists():
            try:
                path.unlink()
                print(f"[InputManager] Archivo temporal eliminado: {path.name}")
            except Exception as e:
                print(f"[InputManager] No se pudo eliminar {path.name}: {e}")
