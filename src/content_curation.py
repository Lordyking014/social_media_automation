import requests
from bs4 import BeautifulSoup
from src.text_generator import _call_gemini, _sanitize_input
from src.news_scraper import fetch_news


def curate_from_rss(feed_url: str, limit: int = 5) -> list:
    articles = []

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(feed_url, headers=headers, timeout=15, verify=True)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item") or soup.find_all("entry")

        for item in items[:limit]:
            title = item.title.get_text(strip=True) if item.title else ""
            description = ""
            if item.description:
                description = item.description.get_text(strip=True)[:200]
            link = ""
            if item.link:
                link = item.link.get("href", "") or item.link.get_text(strip=True)

            if title:
                articles.append({
                    "title": title,
                    "description": description,
                    "link": link,
                    "source": feed_url.split("/")[2],
                })

    except Exception as e:
        print(f"Erro ao acessar feed: {e}")

    return articles


def generate_curated_post(articles: list[dict], tone: str = "profissional") -> dict:
    news_text = "\n".join([
        f"- {a['title']}: {a['description'][:100]}"
        for a in articles[:5]
    ])

    prompt = f"""Crie um post de curadoria com estas noticias:

{news_text}

Formato:
LEGENDA: Post curadoria com CTA
STORIES: 3 slides resumindo
HIGHLIGHTS: 3 destaques principais

Seja informativo e engajante!"""

    response = _call_gemini(prompt)

    result = {
        "articles": articles,
        "curated_post": response,
    }

    print(f"\nPost de curadoria:")
    print(response)

    return result


def curate_and_generate(feed_url: str = None, niche: str = "tech", limit: int = 5) -> dict:
    if feed_url:
        print(f"Buscando de: {feed_url}")
        articles = curate_from_rss(feed_url, limit)
    else:
        print(f"Buscando noticias de {niche}...")
        news = fetch_news(categories=[niche], limit=limit)
        articles = [{"title": n["title"], "description": n["description"], "link": n.get("link", ""), "source": n.get("source", "")} for n in news]

    if not articles:
        print("Nenhum artigo encontrado")
        return {}

    print(f"\n{len(articles)} artigos encontrados:")
    for i, a in enumerate(articles, 1):
        print(f"  {i}. {a['title'][:60]}")

    result = generate_curated_post(articles)
    return result


def suggest_curated_sources(niche: str = "tech") -> dict:
    niche = _sanitize_input(niche)

    prompt = f"""Sugira feeds RSS e sites para curadoria de conteudo de {niche}:

Para cada fonte, inclua:
- NOME: [nome do site]
- URL: [URL do RSS feed]
- TIPO: [noticias/blog/podcast]
- FREQUENCIA: [atualizacao]

Formato:
FONTE_1:
NOME: [nome]
URL: [url]
TIPO: [tipo]
FREQUENCIA: [frequencia]

FONTE_2: ..."""

    response = _call_gemini(prompt)

    print(f"\nFontes sugeridas para {niche}:")
    print(response)

    return {"niche": niche, "sources": response}
