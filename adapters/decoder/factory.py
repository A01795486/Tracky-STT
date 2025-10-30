from pathlib import Path
from adapters.decoder.ogg_opus import OggOpusDecoder
from adapters.decoder.m4a_aac import M4ADecoder
from adapters.decoder.wav_decoder import WavDecoder


class DecoderFactory:
    """
    Fábrica de decodificadores de audio.

    Selecciona el decodificador más adecuado basándose en:
    1. La extensión del archivo (.ogg, .m4a, .wav).
    2. El tipo MIME reportado por FastAPI (audio/ogg, audio/m4a, etc.).
    3. El proveedor declarado, como último recurso.

    Este diseño garantiza que el sistema sea totalmente agnóstico
    al origen del audio, priorizando siempre el formato real del archivo.
    """

    @staticmethod
    def get(provider: str = "", file_path: Path = None, mime_type: str = ""):
        """
        Devuelve el decodificador correcto según formato detectado.

        Argumentos:
            provider: Nombre del proveedor (ej. WhatsApp, Teams, Web).
            file_path: Ruta del archivo temporal.
            mime_type: Tipo MIME reportado por FastAPI o cabecera HTTP.

        Retorna:
            Instancia de decodificador correspondiente.
        """
        provider = (provider or "").strip().upper()
        suffix = file_path.suffix.lower() if file_path else ""
        mime_type = (mime_type or "").lower()

        # --- Detección por MIME type ---
        if mime_type in ["audio/ogg", "audio/opus", "application/ogg"]:
            print("[DecoderFactory] Detección MIME: OGG/Opus.")
            return OggOpusDecoder()
        elif mime_type in ["audio/m4a", "audio/mp4", "audio/aac"]:
            print("[DecoderFactory] Detección MIME: M4A/AAC.")
            return M4ADecoder()
        elif mime_type in ["audio/wav", "audio/x-wav", "audio/vnd.wave"]:
            print("[DecoderFactory] Detección MIME: WAV.")
            return WavDecoder()

        #Detección por extensión 
        if suffix in [".ogg", ".opus"]:
            print("[DecoderFactory] Detección por extensión: OGG/Opus.")
            return OggOpusDecoder()
        elif suffix in [".m4a", ".aac", ".mp4"]:
            print("[DecoderFactory] Detección por extensión: M4A/AAC.")
            return M4ADecoder()
        elif suffix in [".wav"]:
            print("[DecoderFactory] Detección por extensión: WAV.")
            return WavDecoder()

        # Fallback por proveedor
        if provider in ["WA", "WHATSAPP", "TG", "TELEGRAM", "DISCORD", "SLACK"]:
            print("[DecoderFactory] Proveedor detectado: OGG/Opus (WhatsApp/Telegram).")
            return OggOpusDecoder()
        elif provider in ["TEAMS", "MSTEAMS", "MESSENGER", "INSTAGRAM"]:
            print("[DecoderFactory] Proveedor detectado: M4A/AAC (Teams/Messenger).")
            return M4ADecoder()
        elif provider in ["WEB", "TRACKYWEB"]:
            print("[DecoderFactory] Proveedor detectado: WAV (grabación Web).")
            return WavDecoder()

        #Fallback por defectp
        print("[DecoderFactory] Formato desconocido, usando OggOpusDecoder por defecto.")
        return OggOpusDecoder()
