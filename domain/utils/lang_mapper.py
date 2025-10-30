class LanguageMapper:
    """
    Utilidad central para normalizar códigos de idioma según el motor STT.

    Permite traducir automáticamente los códigos ISO o regionales
    al formato esperado por cada proveedor de transcripción.
    """

    @staticmethod
    def for_whisper(lang_code: str) -> str:
        """
        Devuelve el código de idioma compatible con Whisper.
        Ejemplo: 'es-MX' → 'es'
        """
        if not lang_code:
            return "en"
        return lang_code.split("-")[0].lower()

    @staticmethod
    def for_azure(lang_code: str) -> str:
        """
        Devuelve el código de idioma compatible con Azure STT.
        Mapea los idiomas base a los formatos regionales esperados por Azure.
        """
        valid_azure_langs = {
            "es": "es-MX",
            "en": "en-US",
            "pt": "pt-BR",
            "fr": "fr-FR",
            "de": "de-DE",
            "it": "it-IT",
            "ja": "ja-JP",
            "ko": "ko-KR",
            "zh": "zh-CN",
        }
        base = lang_code.split("-")[0].lower() if lang_code else "en"
        return valid_azure_langs.get(base, lang_code or "en-US")

    @staticmethod
    def for_google(lang_code: str) -> str:
        """
        Devuelve el código de idioma compatible con Google STT.
        Actualmente acepta códigos regionales completos.
        """
        return lang_code or "en-US"
