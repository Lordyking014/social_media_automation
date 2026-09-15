from PIL import Image, ImageDraw, ImageFont
import os
import random


TEMPLATE_STYLES = {
    "quote": {
        "name": "Frase Inspiracional",
        "bg_colors": [(26, 26, 46), (45, 45, 80), (15, 15, 30)],
        "text_color": (255, 255, 255),
        "accent_color": (0, 200, 255),
    },
    "tip": {
        "name": "Dica Rapida",
        "bg_colors": [(20, 80, 60), (30, 100, 70), (15, 60, 50)],
        "text_color": (255, 255, 255),
        "accent_color": (0, 255, 150),
    },
    "list": {
        "name": "Lista",
        "bg_colors": [(80, 20, 20), (100, 30, 30), (60, 15, 15)],
        "text_color": (255, 255, 255),
        "accent_color": (255, 200, 0),
    },
    "stats": {
        "name": "Estatistica",
        "bg_colors": [(20, 20, 80), (30, 30, 100), (15, 15, 60)],
        "text_color": (255, 255, 255),
        "accent_color": (0, 150, 255),
    },
    "cta": {
        "name": "Chamada para Acao",
        "bg_colors": [(80, 20, 80), (100, 30, 100), (60, 15, 60)],
        "text_color": (255, 255, 255),
        "accent_color": (255, 0, 200),
    },
    "minimal": {
        "name": "Minimalista",
        "bg_colors": [(250, 250, 250), (240, 240, 240), (245, 245, 245)],
        "text_color": (30, 30, 30),
        "accent_color": (100, 100, 100),
    },
}


def _validate_path(path: str) -> str:
    path = os.path.normpath(path)
    if ".." in path:
        raise ValueError(f"Caminho invalido: {path}")
    return path


def create_template(
    style: str,
    title: str,
    subtitle: str = "",
    output_path: str = None,
    width: int = 1080,
    height: int = 1080,
) -> str:
    if style not in TEMPLATE_STYLES:
        raise ValueError(f"Estilo '{style}' nao encontrado. Opcoes: {', '.join(TEMPLATE_STYLES.keys())}")

    if output_path is None:
        output_path = f"template_{style}.png"
    else:
        output_path = _validate_path(output_path)

    config = TEMPLATE_STYLES[style]
    bg_color = random.choice(config["bg_colors"])

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 64)
        font_sub = ImageFont.truetype("arial.ttf", 32)
    except OSError:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    margin = 80

    draw.rounded_rectangle(
        [margin, margin, width - margin, height - margin],
        radius=30,
        fill=None,
        outline=config["accent_color"],
        width=4,
    )

    words = title.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font_title)
        if bbox[2] - bbox[0] <= width - margin * 3:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)

    total_h = len(lines) * 80
    y_start = (height - total_h) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_title)
        tw = bbox[2] - bbox[0]
        x = (width - tw) // 2
        y = y_start + i * 80
        draw.text((x, y), line, fill=config["text_color"], font=font_title)

    if subtitle:
        bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
        tw = bbox[2] - bbox[0]
        x = (width - tw) // 2
        y = y_start + len(lines) * 80 + 40
        draw.text((x, y), subtitle, fill=config["accent_color"], font=font_sub)

    img.save(output_path, quality=95)
    print(f"Template '{config['name']}' salvo: {output_path}")
    return output_path


def list_templates() -> dict:
    print("\nTemplates disponiveis:")
    for key, data in TEMPLATE_STYLES.items():
        print(f"  {key}: {data['name']}")
    return TEMPLATE_STYLES


def create_templates_batch(texts: list[dict], style: str = "quote") -> list:
    results = []
    for i, item in enumerate(texts):
        path = create_template(
            style=style,
            title=item.get("title", ""),
            subtitle=item.get("subtitle", ""),
            output_path=f"template_{i+1}.png",
        )
        results.append(path)
    return results
