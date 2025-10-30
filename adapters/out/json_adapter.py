import json
from dataclasses import asdict
from domain.entities import TranscriptResult


class JsonResponseAdapter:
    """
    Adaptador de salida para la serialización de respuestas JSON del sistema Tracky STT.

    Centraliza la lógica de formateo y nivel de detalle de la respuesta,
    permitiendo generar salidas compactas o completas de forma agnóstica al proveedor.

    Métodos:
        serialize(result, mode):
            Convierte un objeto TranscriptResult en un diccionario JSON
            listo para ser devuelto por la API.
    """

    @staticmethod
    def serialize(result: TranscriptResult, mode: str = "compact") -> dict:
        """
        Convierte un TranscriptResult en un diccionario JSON serializado.

        Argumentos:
            result: Objeto TranscriptResult proveniente del dominio.
            mode: Nivel de detalle de salida ('compact' o 'full').

        Retorna:
            dict: Estructura JSON lista para enviar como respuesta HTTP.
        """
        data = asdict(result)

        if mode.lower() == "compact":
            data.pop("raw", None)

        return data
