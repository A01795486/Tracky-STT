from typing import Protocol
from pathlib import Path
from domain.entities import TranscriptResult


class AudioDecoderPort(Protocol):
    """
    Puerto (interfaz) para decodificadores de audio.

    Define el contrato que deben cumplir todos los decodificadores
    para transformar cualquier formato de entrada a WAV mono 16 kHz.
    """

    def to_wav_mono16k(self, src: Path) -> Path:
        """Convierte un archivo de audio al formato WAV mono 16 kHz."""
        ...


class NoiseReducerPort(Protocol):
    """
    Puerto (interfaz) para reductores de ruido.

    Define el contrato para todos los componentes que apliquen
    procesos de limpieza o reducción de ruido sobre el audio.
    """

    def reduce(self, wav_path: Path) -> Path:
        """Reduce el ruido del archivo WAV especificado."""
        ...


class TranscriberPort(Protocol):
    """
    Puerto (interfaz) para motores Speech-to-Text (STT).

    Define el contrato que deben cumplir los adaptadores de transcripción,
    asegurando compatibilidad con el dominio.
    """

    def transcribe(self, wav_path: Path, language: str) -> TranscriptResult:
        """Transcribe un archivo de audio al texto correspondiente."""
        ...
