from adapters.stt.whisper_adapter import WhisperAdapter
from adapters.stt.azure_adapter import AzureSTTAdapter
from adapters.stt.google_adapter import GoogleSTTAdapter


class STTFactory:
    """
    Fábrica de motores Speech-to-Text para Tracky STT.

    Selecciona dinámicamente el motor de transcripción a utilizar
    según el valor proporcionado ('whisper', 'azure', 'google').
    Todos los motores devuelven un objeto TranscriptResult.

    Métodos:
        get(engine_name):
            Retorna una instancia del motor STT correspondiente.
    """

    @staticmethod
    def get(engine_name: str):
        """
        Obtiene una instancia del motor STT correspondiente.

        Argumentos:
            engine_name: Nombre del motor de transcripción ('whisper', 'azure', 'google').

        Retorna:
            Instancia de un adaptador que implementa la interfaz TranscriberPort.
        """
        engine_name = (engine_name or "whisper").strip().lower()

        if engine_name == "azure":
            print("[STTFactory] Motor seleccionado: Azure Speech-to-Text")
            return AzureSTTAdapter()

        if engine_name == "google":
            print("[STTFactory] Motor seleccionado: Google Cloud Speech-to-Text")
            return GoogleSTTAdapter()

        print("[STTFactory] Motor seleccionado: Whisper (OpenAI)")
        return WhisperAdapter()
