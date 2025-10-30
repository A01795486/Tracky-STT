from pathlib import Path
from datetime import datetime
from domain.entities import AudioMeta, TranscriptResult
from domain.ports import AudioDecoderPort, NoiseReducerPort, TranscriberPort


class SttService:
    """
    Caso de uso principal del sistema Tracky STT.

    Ejecuta el flujo de decodificación, limpieza y transcripción de audio
    de forma agnóstica respecto al proveedor de STT.

    Métodos:
        run(file_path, meta):
            Procesa el audio, lo transcribe y devuelve un TranscriptResult.
    """

    def __init__(self, decoder: AudioDecoderPort, denoiser: NoiseReducerPort, stt: TranscriberPort):
        self.decoder = decoder
        self.denoiser = denoiser
        self.stt = stt

    def run(self, file_path: Path, meta: AudioMeta) -> TranscriptResult:
        """
        Ejecuta el flujo completo de transcripción.

        Argumentos:
            file_path: Ruta del archivo de audio de entrada.
            meta: Metadatos asociados al audio.

        Retorna:
            TranscriptResult: Resultado estructurado y agnóstico.
        """
        wav = self.decoder.to_wav_mono16k(file_path)
        wav_clean = self.denoiser.reduce(wav)
        result = self.stt.transcribe(wav_clean, language=meta.lang)

        if isinstance(result, TranscriptResult):
            return result

        if isinstance(result, dict):
            text = result.get("text", "")
            confidence = float(result.get("confidence", 0.0))
            raw = result
        else:
            text = str(result)
            confidence = 0.0
            raw = None

        return TranscriptResult(
            text=text,
            confidence=confidence,
            language=meta.lang,
            timestamp=datetime.utcnow(),
            provider=meta.provider,
            original_format=meta.content_type,
            raw=raw,
        )
