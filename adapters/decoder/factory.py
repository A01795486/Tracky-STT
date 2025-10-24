from .ogg_opus import OggOpusDecoder
from .m4a_aac import M4ADecoder
from .wav_decoder import WavDecoder 

class DecoderFactory:

    @staticmethod
    def get(provider: str):
        provider = (provider or "").strip().upper()

        if provider in ["WA", "WHATSAPP", "TG", "TELEGRAM"]:
            print("Usando decoder para WhatsApp/Telegram (OGG-Opus).")
            return OggOpusDecoder()

        elif provider in ["TEAMS", "MSTEAMS"]:
            print("Usando decoder para Microsoft Teams (M4A).")
            return M4ADecoder()

        elif provider in ["WEB", "TRACKYWEB"]:
            print("Usando decoder para Web (WAV 16 kHz).")
            return WavDecoder()

        else:
            print(f"Proveedor no reconocido: {provider}. Usando OggOpusDecoder por defecto.")
            return OggOpusDecoder()
