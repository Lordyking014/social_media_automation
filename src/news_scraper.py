import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


CATEGORIES = {
    "tech": {
        "name": "Tecnologia",
        "keywords": ["tecnologia", "tech", "ia", "inteligencia artificial", "software", "hardware",
                     "startup", "inovacao", "digital", "app", "blockchain", "criptomoeda",
                     "cloud", "computacao", "cyberseguranca", "5g", "robotica", "iot",
                     "machine learning", "deep learning", "automacao", "algoritmo"],
        "rss_feeds": [
            "https://feeds.folha.uol.com.br/tec/rss091.xml",
            "https://g1.globo.com/rss/g1/tecnologia/",
            "https://www.infomoney.com.br/feed/",
            "https://techcrunch.com/feed/",
            "https://www.theverge.com/rss/index.xml",
            "https://feeds.arstechnica.com/arstechnica/index",
        ],
    },
    "marketing": {
        "name": "Marketing",
        "keywords": ["marketing", "publicidade", "propaganda", "branding", "midia social",
                     "instagram", "facebook", "tiktok", "youtube", "seo", "trafego",
                     "conteudo", "influenciador", "campanha", "conversao", "engajamento",
                     "copywriting", "funil", "email marketing", "analytics", "metricas"],
        "rss_feeds": [
            "https://www.marketingdigital.com.br/feed/",
            "https://rockcontent.com/blog/feed/",
            "https://www.neilpatel.com/feed/",
            "https://blog.hubspot.com/marketing/rss.xml",
            "https://contentmarketinginstitute.com/feed/",
        ],
    },
    "business": {
        "name": "Empreendedorismo",
        "keywords": ["empreendedorismo", "negocios", "startup", "investimento", "vendas",
                     "lideranca", "gestao", "financas", "renda", "negocio", "empresa",
                     "sucesso", "estrategia", "inovacao", "disrupt", "escala", "pitch",
                     "accelerator", "venture", "capital", "fundador", "ceo"],
        "rss_feeds": [
            "https://exame.com/feed/",
            "https://www.startse.com/feed",
            "https://empreendedorismovirtual.com.br/feed/",
            "https://www.sebrae.com.br/sites/PortalSebrae/feeds/noticias",
            "https://feeds.bloomberg.com/markets/news.rss",
        ],
    },
}


def _clean_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _fetch_rss(feed_url: str, category: str) -> list:
    articles = []

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(feed_url, headers=headers, timeout=15, verify=True)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "xml")

        items = soup.find_all("item") or soup.find_all("entry")

        for item in items[:10]:
            title = ""
            if item.title:
                title = item.title.get_text(strip=True)

            description = ""
            if item.description:
                description = _clean_html(item.description.get_text(strip=True))
            elif item.summary:
                description = _clean_html(item.summary.get_text(strip=True))

            link = ""
            if item.link:
                link = item.link.get("href", "") or item.link.get_text(strip=True)

            pub_date = ""
            if item.pubDate:
                pub_date = item.pubDate.get_text(strip=True)
            elif item.published:
                pub_date = item.published.get_text(strip=True)

            if title:
                articles.append({
                    "title": title,
                    "description": description[:500],
                    "link": link,
                    "date": pub_date,
                    "source": feed_url.split("/")[2],
                    "category": category,
                })

    except Exception as e:
        print(f"  Erro ao acessar {feed_url}: {e}")

    return articles


def _matches_category(text: str, category: str) -> bool:
    keywords = CATEGORIES.get(category, {}).get("keywords", [])
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)


def fetch_news(categories: list[str] = None, limit: int = 10) -> list:
    if not categories:
        categories = ["tech", "marketing", "business"]

    all_articles = []

    for cat in categories:
        if cat not in CATEGORIES:
            print(f"Categoria '{cat}' nao encontrada")
            continue

        cat_data = CATEGORIES[cat]
        print(f"\nBuscando noticias de {cat_data['name']}...")

        for feed_url in cat_data["rss_feeds"]:
            articles = _fetch_rss(feed_url, cat)
            all_articles.extend(articles)

    unique = []
    seen_titles = set()
    for article in all_articles:
        title_lower = article["title"].lower()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique.append(article)

    filtered = []
    for article in unique:
        text = f"{article['title']} {article['description']}"
        for cat in categories:
            if _matches_category(text, cat):
                article["category"] = cat
                filtered.append(article)
                break

    result = filtered[:limit]

    print(f"\n{len(result)} noticias encontradas:")
    for i, art in enumerate(result, 1):
        print(f"  {i}. [{CATEGORIES[art['category']]['name']}] {art['title'][:80]}")

    return result


def fetch_news_by_topic(topic: str, limit: int = 5) -> list:
    all_articles = []

    for cat, data in CATEGORIES.items():
        for feed_url in data["rss_feeds"]:
            articles = _fetch_rss(feed_url, cat)
            all_articles.extend(articles)

    topic_words = topic.lower().split()
    matched = []

    for article in all_articles:
        text = f"{article['title']} {article['description']}".lower()
        if any(word in text for word in topic_words):
            matched.append(article)

    result = matched[:limit]

    print(f"\n{len(result)} noticias sobre '{topic}':")
    for i, art in enumerate(result, 1):
        print(f"  {i}. {art['title'][:80]}")

    return result
