from pathlib import Path
from pydub import AudioSegment
from domain.ports import AudioDecoderPort


class M4ADecoder(AudioDecoderPort):
    def to_wav_mono16k(self, src: Path) -> Path:
        try:
            print(f"[M4ADecoder] Decodificando archivo: {src.name}")
            audio = AudioSegment.from_file(src, format="m4a")

            if audio.channels > 1:
                audio = audio.set_channels(1)
                print("[M4ADecoder] Convertido a mono.")
            if audio.frame_rate != 16000:
                audio = audio.set_frame_rate(16000)
                print(f"[M4ADecoder] Frecuencia ajustada a 16 kHz (antes: {audio.frame_rate}).")

            out_path = src.with_suffix(".wav")
            audio.export(out_path, format="wav")
            print(f"[M4ADecoder] Archivo convertido exitosamente: {out_path.name}")

            return out_path

        except Exception as e:
            print(f"[M4ADecoder] Error procesando {src.name}: {e}")
            return src
