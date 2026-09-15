from PIL import Image
import os
from src.text_generator import _call_gemini


def analyze_image(image_path: str) -> dict:
    image_path = os.path.normpath(image_path)
    if not os.path.exists(image_path):
        raise ValueError(f"Imagem nao encontrada: {image_path}")

    img = Image.open(image_path)
    width, height = img.size
    format_img = img.format
    mode = img.mode

    prompt = f"""Analise esta imagem e descreva:
- O que esta acontecendo na imagem
- Cores predominantes
- Mood/atmosfera
- Possivel uso (post, story, capa, etc)
- Tema/categoria

Imagem: {width}x{height}, {format_img}, {mode}

Seja especifico e detalhado."""

    response = _call_gemini(prompt)

    result = {
        "path": image_path,
        "dimensions": f"{width}x{height}",
        "format": format_img,
        "analysis": response,
    }

    print(f"Analise da imagem:")
    print(f"  Dimensoes: {width}x{height}")
    print(f"  Formato: {format_img}")
    print(f"\n{response}")

    return result


def generate_caption_from_image(image_path: str, tone: str = "profissional", style: str = "feed") -> str:
    analysis = analyze_image(image_path)

    prompt = f"""Com base nesta analise de imagem, crie uma legenda para Instagram:

ANALISE:
{analysis['analysis']}

ESTILO: {style} (feed, story, reels, carrossel)
TOM: {tone}

Regras:
- Maximo 2200 caracteres
- Comece com gancho forte
- Use emojis com moderacao
- Inclua 3-5 hashtags no final
- Termine com CTA"""

    response = _call_gemini(prompt)

    print(f"\nLegenda gerada:")
    print(response)

    return response


def generate_story_from_image(image_path: str) -> str:
    analysis = analyze_image(image_path)

    prompt = f"""Com base nesta imagem, crie 3 textos para stories:

ANALISE:
{analysis['analysis']}

Formato:
SLIDE 1: [gancho]
SLIDE 2: [informacao]
SLIDE 3: [CTA]

Maximo 120 caracteres por slide."""

    response = _call_gemini(prompt)

    print(f"\nStories gerados:")
    print(response)

    return response
