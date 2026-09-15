import requests
from bs4 import BeautifulSoup
from src.text_generator import _call_gemini, _sanitize_input


def find_trending_topics(niche: str = "all") -> dict:
    niche = _sanitize_input(niche)

    prompt = quiche

    prompt = f"""Quais sao os topics trending AGORA no Brasil para o nicho: {niche}?

Pesquise eliste:
1. TOPICS_EM_ALTA: 5 topics quentes do momento
2. HASHTAGS_TRENDING: 10 hashtags que estao em alta
3. CONTEUDO_SUGERIDO: 3 ideias de conteudo para cada topic
4. MELHOR_MOMENTO: Quando postar sobre cada topic

Formato:
TOPICO_1: [nome do topic]
POR_QUE: [por que esta em alta]
HASHTAGS: [hashtags relacionadas]
IDEIAS: [ideias de conteudo]
MOMENTO: [melhor horario]

TOPICO_2: ..."""

    response = _call_gemini(prompt)

    result = {
        "niche": niche,
        "trends": response,
    }

    print(f"\nTopics trending para '{niche}':")
    print(response)

    return result


def find_viral_content(niche: str = "marketing") -> dict:
    niche = _sanitize_input(niche)

    prompt = f"""Analise o tipo de conteudo viral no Instagram para: {niche}

Identifique:
1. FORMATOS_VIRAL: Quais formatos estao viralizando
2. GANCHOS: Tipos de ganchos que funcionam
3. EXTENSOES: Tempo ideal de video/texto
4. HORARIOS: Quando o conteudo viraliza mais
5. ERROS: O que NAO fazer

Formato:
FORMATOS_VIRAL:
- [formato 1]: [por que funciona]
- [formato 2]: [por que funciona]

GANCHOS:
- [tipo 1]: [exemplo]
- [tipo 2]: [exemplo]

EXTENSOES:
- Reels: [tempo]
- Carrossel: [num slides]

HORARIOS:
- Melhor: [horario]
- Pior: [horario]

ERROS:
- [erro 1]
- [erro 2]"""

    response = _call_gemini(prompt)

    result = {
        "niche": niche,
        "viral_analysis": response,
    }

    print(f"\nAnalise viral para '{niche}':")
    print(response)

    return result


def find_hashtag_trends(platform: str = "instagram") -> dict:
    prompt = f"""Quais hashtags estao em alta agora no {platform}?

Liste:
1. POPULARES: 10 hashtags mais usadas
2. CRESCENTES: 5 hashtags que estao crescendo
3. NICHO_TECH: 5 hashtags de tecnologia
4. NICHO_MARKETING: 5 hashtags de marketing
5. NICHO_NEGOCIOS: 5 hashtags de negocios

Formato:
POPULARES: #tag1 #tag2 ...
CRESCENTES: #tag1 #tag2 ...
TECH: #tag1 #tag2 ...
MARKETING: #tag1 #tag2 ...
NEGOCIOS: #tag1 #tag2 ..."""

    response = _call_gemini(prompt)

    result = {
        "platform": platform,
        "hashtags": response,
    }

    print(f"\nHashtags trending no {platform}:")
    print(response)

    return result
