from pathlib import Path
import pyttsx3
from pydub import AudioSegment


BASE_DIR = Path(__file__).resolve().parent / "samples"
BASE_DIR.mkdir(exist_ok=True)

PHRASES = {
    "whatsapp": "Hola, soy un mensaje de voz enviado desde WhatsApp para probar Tracky STT.",
    "telegram": "Mensaje de prueba grabado desde Telegram para evaluar la transcripción.",
    "teams": "Hola equipo, esta es una nota de voz desde Microsoft Teams.",
    "messenger": "Hola, este mensaje viene de Facebook Messenger para probar la API.",
    "web": "Este audio fue grabado desde la interfaz web de Tracky para prueba."
}


def generate_tts_audio(text: str, out_path: Path):
    """
    Genera un archivo de audio a partir de texto usando pyttsx3.

    Argumentos:
        text: Texto que se convertirá en voz.
        out_path: Ruta donde se guardará el archivo WAV generado.
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.save_to_file(text, str(out_path))
    engine.runAndWait()


def create_provider_audio(provider: str, text: str):
    """
    Crea un archivo de prueba específico para un proveedor.

    Argumentos:
        provider: Nombre del origen del audio (whatsapp, teams, telegram, etc.).
        text: Texto que se convertirá en audio para pruebas.
    """
    wav_path = BASE_DIR / f"{provider}.wav"

    if provider in {"whatsapp", "telegram"}:
        final_path = BASE_DIR / f"{provider}.ogg"
    elif provider in {"teams", "messenger"}:
        final_path = BASE_DIR / f"{provider}.m4a"
    else:
        final_path = wav_path

    generate_tts_audio(text, wav_path)
    audio = AudioSegment.from_wav(wav_path)

    if provider in {"whatsapp", "telegram"}:
        audio.export(final_path, format="ogg", codec="libopus")
    elif provider in {"teams", "messenger"}:
        audio.export(final_path, format="ipod")  # AAC/M4A
    else:
        audio.set_frame_rate(16000).set_channels(1).export(final_path, format="wav")

    print(f"[Tests] Generado audio de prueba para {provider.upper()}: {final_path.name}")


if __name__ == "__main__":
    """
    Ejecuta la generación de audios de prueba para todos los proveedores definidos.

    Genera archivos en la carpeta /samples para validar el flujo de decodificación
    y transcripción del sistema Tracky STT.
    """
    for provider, phrase in PHRASES.items():
        create_provider_audio(provider, phrase)
    print("\n[Tests] Audios de prueba generados en carpeta: samples/")
