import requests
from bs4 import BeautifulSoup
from src.text_generator import _call_gemini


def extract_content_from_url(url: str) -> dict:
    print(f"Extraindo conteudo de: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    title = ""
    if soup.title:
        title = soup.title.string.strip()

    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        meta_desc = meta.get("content", "")

    paragraphs = soup.find_all("p")
    text = " ".join(p.get_text(strip=True) for p in paragraphs[:20])

    result = {
        "url": url,
        "title": title,
        "meta_description": meta_desc,
        "text": text[:3000],
    }

    print(f"Titulo: {title}")
    print(f"Texto extraido: {len(text)} caracteres")

    return result


def generate_post_from_url(url: str, tone: str = "profissional") -> dict:
    content = extract_content_from_url(url)

    prompt = f"""Com base no seguinte conteudo, crie um post para Instagram:

TITULO: {content['title']}
RESUMO: {content['meta_description']}
CONTEUDO: {content['text'][:2000]}

Tom de voz: {tone}

Crie:
1. Legenda para feed (com hashtags)
2. Texto para 3 stories
3. Uma frase de destaque para capa"""

    response = _call_gemini(prompt)

    result = {
        "url": url,
        "source_title": content["title"],
        "generated_content": response,
    }

    print(f"\nConteudo gerado a partir de: {content['title']}")
    return result
