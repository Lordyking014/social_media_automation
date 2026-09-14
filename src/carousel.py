import os
from src.text_generator import _call_gemini
from src.image_generator import generate_image


def generate_carousel(topic: str, num_slides: int = 5, output_dir: str = "carousel") -> dict:
    os.makedirs(output_dir, exist_ok=True)

    prompt = f"""Crie um carrossel para Instagram sobre o tema: {topic}

Crie exatamente {num_slides} slides com titulo e conteudo curto.

Formato exato para cada slide:
SLIDE [numero]:
TITULO: [titulo curto e impactante]
CONTEUDO: [1-2 frases de apoio]

Seja direto, informativo e com linguagem acessivel."""

    response = _call_gemini(prompt)

    slides = []
    current_slide = {}

    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("SLIDE"):
            if current_slide:
                slides.append(current_slide)
            current_slide = {"number": len(slides) + 1, "title": "", "content": ""}
        elif line.startswith("TITULO:"):
            current_slide["title"] = line.replace("TITULO:", "").strip()
        elif line.startswith("CONTEUDO:"):
            current_slide["content"] = line.replace("CONTEUDO:", "").strip()

    if current_slide:
        slides.append(current_slide)

    print(f"Gerando {len(slides)} imagens para o carrossel...")
    generated_images = []

    for i, slide in enumerate(slides):
        image_prompt = f"A clean, modern social media slide design with title: '{slide['title']}', minimalist, professional, bold typography style, vibrant gradient background, no text rendered, high quality"
        image_path = os.path.join(output_dir, f"slide_{i+1}.png")
        generate_image(image_prompt, image_path)
        slide["image_path"] = image_path
        generated_images.append(image_path)
        print(f"  Slide {i+1}/{len(slides)}: {slide['title']}")

    result = {
        "topic": topic,
        "total_slides": len(slides),
        "slides": slides,
        "image_paths": generated_images,
        "output_dir": output_dir,
    }

    print(f"\nCarrossel gerado: {len(slides)} slides em '{output_dir}/'")
    return result
