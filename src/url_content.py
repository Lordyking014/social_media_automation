import ipaddress
import socket
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from src.text_generator import _call_gemini, _sanitize_input


BLOCKED_HOSTS = {
    "localhost", "127.0.0.1", "0.0.0.0", "::1",
    "169.254.169.254", "metadata.google.internal",
}


def _validate_url(url: str) -> str:
    url = url.strip()

    parsed = urlparse(url)
    if parsed.scheme not in ("https", "http"):
        raise ValueError(f"Esquema nao permitido: {parsed.scheme}. Use https://")

    if not parsed.hostname:
        raise ValueError("URL invalida: hostname nao encontrado")

    hostname = parsed.hostname.lower()

    if hostname in BLOCKED_HOSTS:
        raise ValueError(f"Hostname bloqueado: {hostname}")

    if hostname.startswith("127.") or hostname.startswith("10.") or hostname.startswith("192.168.") or hostname.startswith("172."):
        raise ValueError(f"IP privado bloqueado: {hostname}")

    try:
        ip = socket.gethostbyname(hostname)
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
            raise ValueError(f"IP interno bloqueado: {ip}")
    except socket.gaierror:
        raise ValueError(f"Nao foi possivel resolver: {hostname}")

    return url


def extract_content_from_url(url: str) -> dict:
    url = _validate_url(url)
    print(f"Extraindo conteudo de: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html",
        "Accept-Language": "pt-BR,pt;q=0.9",
    }

    response = requests.get(url, headers=headers, timeout=30, verify=True, allow_redirects=False)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        raise ValueError(f"Tipo de conteudo nao suportado: {content_type}")

    if len(response.content) > 5 * 1024 * 1024:
        raise ValueError("Pagina muito grande (max 5MB)")

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "iframe", "noscript"]):
        tag.decompose()

    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()[:200]

    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        meta_desc = meta.get("content", "")[:500]

    paragraphs = soup.find_all("p")
    text = " ".join(p.get_text(strip=True) for p in paragraphs[:15])
    text = text[:3000]

    result = {
        "url": url,
        "title": title,
        "meta_description": meta_desc,
        "text": text,
    }

    print(f"Titulo: {title}")
    print(f"Texto extraido: {len(text)} caracteres")

    return result


def generate_post_from_url(url: str, tone: str = "profissional") -> dict:
    content = extract_content_from_url(url)
    tone = _sanitize_input(tone, 50)

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
