from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any, Dict


@dataclass
class AudioMeta:
    """
    Contiene los metadatos del audio procesado por el sistema.

    Atributos:
        provider: Proveedor o fuente del audio (por ejemplo, WhatsApp, Teams).
        content_type: Tipo MIME o formato original del archivo.
        lang: Código del idioma (por defecto "es").
    """
    provider: str
    content_type: str
    lang: str = "es"


@dataclass
class TranscriptResult:
    """
    Representa el resultado de una transcripción de audio.

    Es agnóstica al proveedor de STT e incluye el payload
    completo retornado por el servicio correspondiente.

    Atributos:
        text: Texto transcrito final.
        confidence: Nivel de confianza del modelo.
        language: Idioma detectado o configurado.
        timestamp: Fecha y hora de la transcripción.
        provider: Proveedor de STT utilizado.
        original_format: Formato original del audio.
        raw: Respuesta completa del proveedor (JSON u objeto análogo).
    """
    text: str
    confidence: float
    language: str
    timestamp: datetime
    provider: str
    original_format: str
    raw: Optional[Dict[str, Any]] = field(default=None)
