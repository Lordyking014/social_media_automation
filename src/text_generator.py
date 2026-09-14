import time
import requests
import config


API_KEY = config.GEMINI_API_KEY
MODEL = "gemini-flash-latest"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


def _call_gemini(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    for attempt in range(5):
        try:
            response = requests.post(
                f"{API_URL}?key={API_KEY}",
                headers=headers,
                json=payload,
                timeout=120,
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
                continue

            response.raise_for_status()

        except requests.exceptions.Timeout:
            print(f"  Timeout, tentando novamente... (tentativa {attempt+1}/5)")
            time.sleep(5)

    raise RuntimeError("Numero maximo de tentativas atingido")


def generate_feed_caption(topic: str, tone: str = "profissional") -> str:
    prompt = f"""Crie uma legenda para post de feed no Instagram sobre o tema: {topic}

Tom de voz: {tone}
Requisitos:
- Máximo de 2200 caracteres
- Inclua 3-5 hashtags relevantes no final
- Seja engaging e incentive interação
- Comece com um gancho forte na primeira linha
- Use emojis com moderação
- Estrutura: gancho + conteúdo + CTA + hashtags"""

    return _call_gemini(prompt)


def generate_story_text(topic: str, tone: str = "profissional") -> str:
    prompt = f"""Crie textos curtos para stories do Instagram sobre o tema: {topic}

Tom de voz: {tone}
Requisitos:
- Texto curto e impactante (máximo 120 caracteres por slide)
- Crie 3 slides diferentes
- Slide 1: Gancho/curiosidade
- Slide 2: Informação principal
- Slide 3: CTA ou chamada para ação
- Use linguagem informal e direta
- Formato:
SLIDE 1: [texto]
SLIDE 2: [texto]
SLIDE 3: [texto]"""

    return _call_gemini(prompt)


def generate_image_prompt(topic: str, style: str = "moderno e minimalista") -> str:
    return f"Uma ilustração limpa, moderna e minimalista sobre {topic}, estilo {style}, post profissional para redes sociais, cores vibrantes, iluminação suave, sem texto, alta qualidade, 1080x1080"
