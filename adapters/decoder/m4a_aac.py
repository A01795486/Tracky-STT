from pathlib import Path
from pydub import AudioSegment
from domain.ports import AudioDecoderPort


class M4ADecoder(AudioDecoderPort):
    """
    Decoder de archivos de audio en formato M4A/AAC.

    Convierte archivos utilizados por plataformas como Microsoft Teams
    o Messenger al formato WAV mono 16 kHz, garantizando compatibilidad
    con los motores de transcripción de Tracky STT.

    Métodos:
        to_wav_mono16k(src):
            Convierte el archivo M4A/AAC a formato WAV mono 16 kHz
            y devuelve la ruta del archivo resultante.
    """

    def to_wav_mono16k(self, src: Path) -> Path:
        """
        Convierte un archivo M4A/AAC al formato WAV mono 16 kHz.

        Argumentos:
            src: Ruta del archivo de audio fuente (.m4a o .aac).

        Retorna:
            Path: Ruta del archivo convertido (.wav).
        """
        try:
            print(f"[M4ADecoder] Decodificando archivo: {src.name}")
            audio = AudioSegment.from_file(src, format="m4a")

            if audio.channels > 1:
                audio = audio.set_channels(1)
                print("[M4ADecoder] Convertido a mono.")

            if audio.frame_rate != 16000:
                audio = audio.set_frame_rate(16000)
                print("[M4ADecoder] Frecuencia ajustada a 16 kHz.")

            out_path = src.with_suffix(".wav")
            audio.export(out_path, format="wav")

            print(f"[M4ADecoder] Archivo convertido exitosamente: {out_path.name}")
            return out_path

        except Exception as e:
            print(f"[M4ADecoder] Error procesando {src.name}: {e}")
            return src
