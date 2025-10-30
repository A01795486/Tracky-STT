from fastapi import UploadFile, HTTPException
from pathlib import Path
import base64
import requests


class InputManager:
    """
    Administrador de entradas de audio para Tracky STT.

    Gestiona la recepción de archivos de audio en diferentes formatos
    (archivo cargado, URL remota o cadena Base64) y los almacena
    temporalmente para su posterior procesamiento.

    Métodos:
        process_input(file, audio_url, audio_base64):
            Procesa la entrada recibida y devuelve la ruta del archivo temporal.
    """

    def __init__(self, tmp_dir: str = "./tmp"):
        self.tmp_dir = Path(tmp_dir)
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def process_input(
        self,
        file: UploadFile = None,
        audio_url: str = None,
        audio_base64: str = None
    ) -> Path:
        """
        Procesa el origen del audio (archivo, URL o Base64) y lo guarda temporalmente.

        Argumentos:
            file: Archivo de audio cargado por el usuario.
            audio_url: URL remota que apunta al audio.
            audio_base64: Cadena Base64 del audio.

        Retorna:
            Path: Ruta del archivo temporal.

        Lanza:
            HTTPException: Si ninguna fuente válida fue proporcionada.
        """
        if file:
            tmp = self.tmp_dir / file.filename
            tmp.write_bytes(file.file.read())
            return tmp

        if audio_url:
            tmp = self.tmp_dir / "remote_audio.wav"
            try:
                response = requests.get(audio_url, timeout=15)
                response.raise_for_status()
                tmp.write_bytes(response.content)
                return tmp
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error descargando audio remoto: {e}")

        if audio_base64:
            tmp = self.tmp_dir / "base64_audio.wav"
            try:
                audio_data = base64.b64decode(audio_base64)
                tmp.write_bytes(audio_data)
                return tmp
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error procesando audio Base64: {e}")

        raise HTTPException(status_code=400, detail="Debe enviarse un archivo, URL o Base64 de audio.")
