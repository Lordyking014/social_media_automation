import os
import urllib.parse
import requests


ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024


def _validate_path(path: str, must_exist: bool = False) -> str:
    path = os.path.normpath(path)
    if ".." in path:
        raise ValueError(f"Caminho invalido: {path}")
    if must_exist and not os.path.exists(path):
        raise ValueError(f"Arquivo nao existe: {path}")
    return path


def _validate_output_path(path: str) -> str:
    path = os.path.normpath(path)
    if ".." in path:
        raise ValueError(f"Caminho invalido: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extensao nao permitida: {ext}. Use: {', '.join(ALLOWED_EXTENSIONS)}")
    return path


def _validate_image_response(response: requests.Response, output_path: str):
    content_type = response.headers.get("Content-Type", "")
    if not any(t in content_type for t in ["image/", "application/octet-stream"]):
        raise ValueError(f"Resposta nao e imagem: {content_type}")

    if len(response.content) > MAX_IMAGE_SIZE:
        raise ValueError(f"Imagem muito grande: {len(response.content)} bytes (max {MAX_IMAGE_SIZE})")

    magic_bytes = response.content[:8]
    is_image = (
        magic_bytes[:8] == b"\x89PNG\r\n\x1a\n" or
        magic_bytes[:3] == b"\xff\xd8\xff" or
        magic_bytes[:4] == b"RIFF" or
        b"JFIF" in magic_bytes[:12] or
        b"Exif" in magic_bytes[:12]
    )
    if not is_image:
        raise ValueError(" Conteudo nao e uma imagem valida")


def generate_image(prompt: str, output_path: str = "generated_image.png") -> str:
    output_path = _validate_output_path(output_path)

    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"

    print(f"Gerando imagem com Pollinations.ai...")
    response = requests.get(url, timeout=120, verify=True)
    response.raise_for_status()

    _validate_image_response(response, output_path)

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Imagem salva em: {output_path}")
    return output_path


def generate_image_from_topic(topic: str, output_path: str = "generated_image.png") -> str:
    output_path = _validate_output_path(output_path)

    from src.text_generator import generate_image_prompt

    prompt = generate_image_prompt(topic)
    print(f"Prompt gerado: {prompt}")

    return generate_image(prompt, output_path)
