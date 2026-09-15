from src.text_generator import _call_gemini, _sanitize_input


def optimize_caption_seo(caption: str, target_keyword: str = None) -> dict:
    caption = _sanitize_input(caption, 2000)
    keyword_text = f"Palavra-chave alvo: {target_keyword}" if target_keyword else "Escolha a melhor palavra-chave"

    prompt = f"""Otimize esta legenda para SEO no Instagram:

LEGENDA ATUAL:
{caption}

{keyword_text}

Analise e melhore:
1. PALAVRA_CHAVE: Sugira palavra-chave principal
2. HASHTAGS: Sugira hashtags otimizadas (mix de populares + nichadas)
3. PRIMEIRA_LINHA: Melhore o gancho para maior retencao
4. EMOJI_TAGS: Adicione emojis estrategicos
5. CTA: Melhore a chamada para acao
6. COMPRIMENTO: Verifique se esta no ideal (135-150 chars antes do "mais")

Formato:
PALAVRA_CHAVE: [keyword]
HASHTAGS_OTIMIZADAS: [hashtags]
LEGENDA_MELHORADA: [legenda completa otimizada]
DICAS: [dicas extras]"""

    response = _call_gemini(prompt)

    result = {
        "original": caption,
        "optimized": response,
    }

    print(f"\nLegenda otimizada para SEO:")
    print(response)

    return result


def generate_seo_hashtags(topic: str, platform: str = "instagram") -> dict:
    topic = _sanitize_input(topic)

    prompt = f"""Crie hashtags SEO otimizadas para {platform} sobre: {topic}

Regras:
- 3 hashtags populares (1M+ posts)
- 5 hashtags medias (100k-1M)
- 7 hashtags nichadas (<100k)
- Todas relevantes ao tema
- Em portugues brasileiro

Formato:
POPULARES: #tag1 #tag2 #tag3
MEDIAS: #tag1 #tag2 #tag3 #tag4 #tag5
NICHADAS: #tag1 #tag2 #tag3 #tag4 #tag5 #tag6 #tag7
TODAS: [todas juntas]"""

    response = _call_gemini(prompt)

    result = {
        "topic": topic,
        "platform": platform,
        "hashtags": response,
    }

    print(f"\nHashtags SEO para '{topic}' em {platform}:")
    print(response)

    return result


def analyze_post_seo(caption: str) -> dict:
    caption = _sanitize_input(caption, 2000)

    prompt = f"""Analise o SEO desta legenda de Instagram:

{caption}

Analise:
1. NOTA_GERAL: 1-10
2. COMPRIMENTO: Ideal/Muito curto/Muito longo
3. HASHTAGS: Quantidade e qualidade
4. KEYWORDS: Palavras-chave presentes
5. CTA: Tem chamada para acao?
6. PRIMEIRA_LINHA: Gancho forte?
7. EMOJI: Uso adequado?
8. MELHORIAS: Lista de melhorias

Formato:
NOTA_GERAL: [nota]/10
COMPRIMENTO: [status]
HASHTAGS: [analise]
KEYWORDS: [keywords encontradas]
CTA: [Sim/Nao + sugestao]
PRIMEIRA_LINHA: [analise]
EMOJI: [analise]
MELHORIAS: [lista de melhorias]"""

    response = _call_gemini(prompt)

    result = {
        "caption": caption,
        "analysis": response,
    }

    print(f"\nAnalise SEO:")
    print(response)

    return result
