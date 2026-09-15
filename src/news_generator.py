from src.text_generator import _call_gemini, _sanitize_input
from src.news_scraper import fetch_news, fetch_news_by_topic, CATEGORIES


def generate_post_from_news(article: dict, tone: str = "profissional") -> dict:
    prompt = f"""Com base nesta noticia, crie um post completo para Instagram:

TITULO: {article['title']}
RESUMO: {article['description']}
CATEGORIA: {CATEGORIES.get(article['category'], {}).get('name', article['category'])}

Crie:
1. LEGENDA: Legenda engaging com gancho, conteudo e CTA (max 2200 chars)
2. STORIES: 3 texts curtos para stories
3. HASHTAGS: 5 hashtags relevantes

Formato:
LEGENDA: [legenda completa]
STORY_1: [texto]
STORY_2: [texto]
STORY_3: [texto]
HASHTAGS: #tag1 #tag2 #tag3 #tag4 #tag5"""

    response = _call_gemini(prompt)

    result = {
        "source": article,
        "caption": "",
        "stories": [],
        "hashtags": "",
    }

    current_field = ""
    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("LEGENDA:"):
            result["caption"] = line.replace("LEGENDA:", "").strip()
            current_field = "caption"
        elif line.startswith("STORY_"):
            result["stories"].append(line.split(":", 1)[1].strip() if ":" in line else "")
        elif line.startswith("HASHTAGS:"):
            result["hashtags"] = line.replace("HASHTAGS:", "").strip()
        elif current_field == "caption" and line:
            result["caption"] += "\n" + line

    return result


def generate_daily_news_post(categories: list[str] = None, tone: str = "profissional") -> dict:
    if not categories:
        categories = ["tech", "marketing", "business"]

    print("Buscando noticias mais recentes...")
    news = fetch_news(categories=categories, limit=5)

    if not news:
        print("Nenhuma noticia encontrada")
        return {}

    print(f"\nGerando post a partir de: {news[0]['title']}")
    result = generate_post_from_news(news[0], tone)

    result["all_news"] = news
    result["selected"] = news[0]

    print(f"\nLegenda gerada:")
    print(result["caption"])

    print(f"\nStories:")
    for s in result["stories"]:
        print(f"  - {s}")

    print(f"\nHashtags: {result['hashtags']}")

    return result


def generate_news_roundup(categories: list[str] = None, count: int = 3) -> dict:
    if not categories:
        categories = ["tech", "marketing", "business"]

    print(f"Buscando top {count} noticias...")
    news = fetch_news(categories=categories, limit=count)

    if not news:
        return {}

    news_text = "\n".join([
        f"{i+1}. {n['title']} - {n['description'][:100]}"
        for i, n in enumerate(news)
    ])

    prompt = f"""Crie um post resumo das noticias mais importantes do dia:

{news_text}

Formato:
LEGENDA: Resumo das 3 noticias com CTA
STORY_TITULO: Titulo chamativo para story
HIGHLIGHTS: 3 bullets com destaques"""

    response = _call_gemini(prompt)

    result = {
        "news": news,
        "roundup": response,
    }

    print(f"\nResumo diario:")
    print(response)

    return result


def generate_weekly_newsletter(niche: str = "tech") -> dict:
    print(f"Buscando noticias da semana de {niche}...")
    news = fetch_news(categories=[niche], limit=10)

    if not news:
        return {}

    news_text = "\n".join([
        f"{i+1}. {n['title']}"
        for i, n in enumerate(news)
    ])

    prompt = f"""Crie uma newsletter semanal de {niche} para Instagram:

NOTICIAS DA SEMANA:
{news_text}

Formato:
ASSUNTO: Titulo chamativo da newsletter
INTRODUCAO: 2-3 frases de abertura
TOP_3: 3 noticias mais importantes
DESTAQUE: 1 noticia para profundidade
CTA: Chamada para acao

Seja informativo e engajante!"""

    response = _call_gemini(prompt)

    result = {
        "niche": niche,
        "news_count": len(news),
        "newsletter": response,
    }

    print(f"\nNewsletter {niche}:")
    print(response)

    return result
