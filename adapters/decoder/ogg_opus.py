from pathlib import Path
from pydub import AudioSegment
from domain.ports import AudioDecoderPort


class OggOpusDecoder(AudioDecoderPort):
    """
    Decoder de archivos de audio en formato OGG/Opus.

    Convierte cualquier archivo .ogg o .opus a formato WAV
    con frecuencia de muestreo de 16 kHz y canal mono,
    garantizando compatibilidad con los motores STT.

    Métodos:
        to_wav_mono16k(src):
            Convierte el archivo a formato WAV mono 16 kHz y devuelve la ruta resultante.
    """

    def to_wav_mono16k(self, src: Path) -> Path:
        """
        Convierte un archivo OGG/Opus al formato WAV mono 16 kHz.

        Argumentos:
            src: Ruta del archivo de audio fuente (.ogg o .opus).

        Retorna:
            Path: Ruta del archivo convertido (.wav).
        """
        try:
            audio = AudioSegment.from_file(src)
            audio = audio.set_frame_rate(16000).set_channels(1)

            out = src.with_suffix(".wav")
            audio.export(out, format="wav")

            print(f"[OggOpusDecoder] Archivo convertido correctamente: {out.name}")
            return out

        except Exception as e:
            print(f"[OggOpusDecoder] Error procesando {src.name}: {e}")
            return src
