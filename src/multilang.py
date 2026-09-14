from src.text_generator import _call_gemini


LANGUAGES = {
    "pt": "portugues brasileiro",
    "en": "ingles",
    "es": "espanhol",
    "fr": "frances",
    "de": "alemao",
    "it": "italiano",
    "ja": "japones",
    "ko": "coreano",
    "zh": "chines",
    "ar": "arabe",
    "ru": "russo",
}


def translate_caption(caption: str, target_lang: str = "en") -> str:
    lang_name = LANGUAGES.get(target_lang, target_lang)

    prompt = f"""Traduza esta legenda de Instagram para {lang_name}:

LEGENDA ORIGINAL:
{caption}

Regras:
- Mantenha o tom e estilo original
- Adapte expressoes idiomáticas
- Mantenha emojis no mesmo lugar
- Hashtags devem ser traduzidas ou adaptadas para o idioma alvo
- Nao adicione texto extra"""

    response = _call_gemini(prompt)

    print(f"\nTraducao para {lang_name}:")
    print(response)

    return response.strip()


def translate_batch(caption: str, languages: list[str] = None) -> dict:
    if not languages:
        languages = ["en", "es", "fr"]

    results = {"original": caption, "translations": {}}

    for lang in languages:
        translation = translate_caption(caption, lang)
        results["translations"][lang] = translation

    print(f"\nTraducoes completas:")
    for lang, text in results["translations"].items():
        print(f"\n[{lang.upper()}]")
        print(text[:100] + "...")

    return results


def create_multilingual_post(topic: str, languages: list[str] = None) -> dict:
    if not languages:
        languages = ["pt", "en", "es"]

    results = {"topic": topic, "languages": {}}

    for lang in languages:
        lang_name = LANGUAGES.get(lang, lang)

        prompt = f"""Crie uma legenda para Instagram sobre: {topic}
Idioma: {lang_name}
Maximo 200 caracteres com hashtags"""

        caption = _call_gemini(prompt)
        results["languages"][lang] = caption.strip()

        print(f"\n[{lang.upper()}] {lang_name}:")
        print(caption.strip())

    return results


def detect_language(text: str) -> str:
    prompt = f"""Detecte o idioma deste texto e responda APENAS com o codigo ISO 639-1 (2 letras):

TEXTO: {text[:200]}

CODIGO:"""

    response = _call_gemini(prompt)
    return response.strip().lower()


def get_supported_languages() -> dict:
    print("\nIdiomas suportados:")
    for code, name in LANGUAGES.items():
        print(f"  {code}: {name}")
    return LANGUAGES
