from pathlib import Path
from pydub import AudioSegment
from domain.ports import AudioDecoderPort

class OggOpusDecoder(AudioDecoderPort):
    def to_wav_mono16k(self, src: Path) -> Path:
        audio = AudioSegment.from_file(src)
        audio = audio.set_frame_rate(16000).set_channels(1)
        out = src.with_suffix(".wav")
        audio.export(out, format="wav")
        return out
    