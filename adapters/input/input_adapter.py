import base64
from pathlib import Path
import uuid


class InputAdapter:
    """
    Adaptador de entrada Base64 para Tracky STT.

    Convierte una cadena Base64 en un archivo WAV temporal,
    garantizando un identificador único para evitar colisiones
    y facilitar el procesamiento concurrente.

    Métodos:
        get_audio_input(audio_base64):
            Decodifica la cadena Base64 y guarda el archivo WAV temporal.
    """

    @staticmethod
    def get_audio_input(audio_base64: str) -> Path:
        """
        Decodifica un audio Base64 y lo guarda como archivo WAV temporal.

        Argumentos:
            audio_base64: Cadena Base64 que representa el audio.

        Retorna:
            Path: Ruta del archivo WAV temporal.

        Lanza:
            ValueError: Si no se proporciona audio o la decodificación falla.
        """
        if not audio_base64:
            raise ValueError("No se proporcionó audio en formato Base64.")

        try:
            audio_data = base64.b64decode(audio_base64)
            tmp_file = Path(f"./tmp/{uuid.uuid4()}_base64.wav")
            tmp_file.parent.mkdir(parents=True, exist_ok=True)
            tmp_file.write_bytes(audio_data)
            print(f"[InputAdapter] Audio Base64 decodificado: {tmp_file.name}")
            return tmp_file

        except Exception as e:
            raise ValueError(f"Error procesando audio Base64: {e}")
