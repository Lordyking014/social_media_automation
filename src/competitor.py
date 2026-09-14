import requests
from bs4 import BeautifulSoup
from src.text_generator import _call_gemini


def analyze_competitor(username: str, platform: str = "instagram") -> dict:
    print(f"\nAnalizando concorrente: {username} ({platform})")

    prompt = f"""Simule uma analise de perfil de concorrente no Instagram:

PERFIL: @{username}
PLATAFORMA: {platform}

Com base em perfis similares ao nicho, crie uma analise completa:

PERFIL:
- Nicho identificado: [nicho]
- Frequencia de posts: [x posts/semana]
- Melhor horario: [horario]
- Tom de voz: [tom]
- Pontos fortes: [lista]
- Pontos fracos: [lista]

ESTRATEGIA:
- Tipo de conteudo que funciona: [tipos]
- Formatos mais usados: [formatos]
- Hashtags estrategicas: [hashtags]
- Taxa de engajamento estimada: [%]

SUGESTOES:
1. [sugestao 1]
2. [sugestao 2]
3. [sugestao 3]

CONTEUDO para copiar a estrategia:
- 3 ideias de posts baseados nesse concorrente"""

    response = _call_gemini(prompt)

    result = {
        "username": username,
        "platform": platform,
        "analysis": response,
    }

    print(f"\nAnalise de @{username}:")
    print(response)

    return result


def generate_competitor_content(analysis: str, topic: str = None) -> dict:
    prompt = f"""Com base nesta analise de concorrente, gere conteudo original:

ANALISE:
{analysis[:2000]}

Crie 3 posts originais inspirados na estrategia mas com conteudo unico:
1. Post educativo
2. Post de engajamento
3. Post de valor

Formato:
POST_1 (EDUCATIVO):
TEMA: [tema]
LEGENDA: [legenda completa]

POST_2 (ENGAJAMENTO):
TEMA: [tema]
LEGENDA: [legenda completa]

POST_3 (VALOR):
TEMA: [tema]
LEGENDA: [legenda completa]"""

    response = _call_gemini(prompt)

    result = {"raw": response, "posts": []}
    current_post = {}

    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("POST_"):
            if current_post:
                result["posts"].append(current_post)
            current_post = {"type": line, "theme": "", "caption": ""}
        elif line.startswith("TEMA:"):
            current_post["theme"] = line.replace("TEMA:", "").strip()
        elif line.startswith("LEGENDA:"):
            current_post["caption"] = line.replace("LEGENDA:", "").strip()

    if current_post:
        result["posts"].append(current_post)

    print(f"\nConteudo inspirado no concorrente:")
    for p in result["posts"]:
        print(f"\n  [{p.get('type', '')}] {p.get('theme', '')}")
        print(f"  {p.get('caption', '')[:100]}...")

    return result


def find_competitors(niche: str) -> list:
    prompt = f"""Sugira 5 perfis de concorrentes/benchmark no Instagram para o nicho: {niche}

Para cada perfil, diga:
- @username
- Por que e um bom benchmark
- Numero seguidores (estimativa)

Formato:
1. @username - [motivo] - [seguidores]
2. ..."""

    response = _call_gemini(prompt)

    print(f"\nConcorrentes sugeridos para {niche}:")
    print(response)

    return {"niche": niche, "competitors": response}
