import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.text_generator import _call_gemini


def generate_reels_script(topic: str, duration: int = 30, tone: str = "casual") -> dict:
    prompt = f"""Crie um roteiro completo para um video curto (Reels/TikTok) sobre o tema: {topic}

Duracao: {duration} segundos
Tom de voz: {tone}

Formato exato:
GANCHO (primeiros 3s): [frase impactante]
DESENVOLVIMENTO: [conteudo principal em 2-3 pontos rapidos]
CTA (ultimos 3s): [chamada para acao]

Tambem inclua:
- SUGESTAO_VISUAL: Descricao do que mostrar em cada parte
- MUSICA: Tipo de musica de fundo sugerida
-Legendas: Sim/Nao

Responda no formato:
GANCHO: [texto]
DESENVOLVIMENTO: [texto]
CTA: [texto]
SUGESTAO_VISUAL: [descricao]
MUSICA: [tipo]
LEGENDAS: [Sim/Nao]"""

    response = _call_gemini(prompt)

    result = {
        "topic": topic,
        "duration": duration,
        "raw_script": response,
    }

    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("GANCHO:"):
            result["hook"] = line.replace("GANCHO:", "").strip()
        elif line.startswith("DESENVOLVIMENTO:"):
            result["development"] = line.replace("DESENVOLVIMENTO:", "").strip()
        elif line.startswith("CTA:"):
            result["cta"] = line.replace("CTA:", "").strip()
        elif line.startswith("SUGESTAO_VISUAL:"):
            result["visual"] = line.replace("SUGESTAO_VISUAL:", "").strip()
        elif line.startswith("MUSICA:"):
            result["music"] = line.replace("MUSICA:", "").strip()
        elif line.startswith("LEGENDAS:"):
            result["subtitles"] = line.replace("LEGENDAS:", "").strip()

    return result


def generate_reels_caption(topic: str, tone: str = "casual") -> str:
    prompt = f"""Crie uma legenda curta e chamativa para um video de Reels/TikTok sobre: {topic}

Tom: {tone}
Requisitos:
- Maximo 150 caracteres
- Use emojis
- Inclua 3 hashtags
- Termine com um CTA"""

    return _call_gemini(prompt)
