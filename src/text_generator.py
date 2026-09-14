import re
import time
import requests
import config


API_KEY = config.GEMINI_API_KEY
MODEL = "gemini-flash-latest"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

_last_api_call = 0
MIN_API_INTERVAL = 2


def _sanitize_input(text: str, max_length: int = 500) -> str:
    text = text.strip()[:max_length]
    text = re.sub(r"[^\w\sàáâãéêíóôõúüç.,!?\-#@]", "", text, flags=re.IGNORECASE)
    return text


def _rate_limit():
    global _last_api_call
    elapsed = time.time() - _last_api_call
    if elapsed < MIN_API_INTERVAL:
        time.sleep(MIN_API_INTERVAL - elapsed)
    _last_api_call = time.time()


def _call_gemini(prompt: str) -> str:
    _rate_limit()

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    for attempt in range(5):
        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=120,
                verify=True,
            )
            if response.status_code == 200:
                return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

            data = response.json()
            retry_after = 20

            if "error" in data and "details" in data["error"]:
                for detail in data["error"]["details"]:
                    if detail.get("@type", "").endswith("RetryInfo"):
                        retry_after = int(detail.get("retryDelay", "15s").replace("s", ""))
                        break

            if response.status_code in (429, 503):
                print(f"  Limite atingido, aguardando {retry_after}s... (tentativa {attempt+1}/5)")
                time.sleep(retry_after + 1)
                _rate_limit()
                continue

            response.raise_for_status()

        except requests.exceptions.Timeout:
            print(f"  Timeout, tentando novamente... (tentativa {attempt+1}/5)")
            time.sleep(5)

    raise RuntimeError("Numero maximo de tentativas atingido")


def generate_feed_caption(topic: str, tone: str = "profissional") -> str:
    topic = _sanitize_input(topic)
    tone = _sanitize_input(tone, 50)

    prompt = f"""Crie uma legenda para post de feed no Instagram sobre o tema: {topic}

Tom de voz: {tone}
Requisitos:
- Maximo de 2200 caracteres
- Inclua 3-5 hashtags relevantes no final
- Seja engaging e incentive interacao
- Comece com um gancho forte na primeira linha
- Use emojis com moderacao
- Estrutura: gancho + conteudo + CTA + hashtags"""

    return _call_gemini(prompt)


def generate_story_text(topic: str, tone: str = "profissional") -> str:
    topic = _sanitize_input(topic)
    tone = _sanitize_input(tone, 50)

    prompt = f"""Crie textos curtos para stories do Instagram sobre o tema: {topic}

Tom de voz: {tone}
Requisitos:
- Texto curto e impactante (maximo 120 caracteres por slide)
- Crie 3 slides diferentes
- Slide 1: Gancho/curiosidade
- Slide 2: Informacao principal
- Slide 3: CTA ou chamada para acao
- Use linguagem informal e direta
- Formato:
SLIDE 1: [texto]
SLIDE 2: [texto]
SLIDE 3: [texto]"""

    return _call_gemini(prompt)


def generate_image_prompt(topic: str, style: str = "moderno e minimalista") -> str:
    topic = _sanitize_input(topic)
    return f"Uma ilustracao limpa, moderna e minimalista sobre {topic}, estilo {style}, post profissional para redes sociais, cores vibrantes, iluminacao suave, sem texto, alta qualidade, 1080x1080"
