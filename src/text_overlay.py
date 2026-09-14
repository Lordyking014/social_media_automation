from PIL import Image, ImageDraw, ImageFont
import os


def _validate_path(path: str, check_exists: bool = False) -> str:
    path = os.path.normpath(path)
    if ".." in path:
        raise ValueError(f"Caminho invalido: {path}")
    if check_exists and not os.path.exists(path):
        raise ValueError(f"Arquivo nao existe: {path}")
    return path


def add_text_overlay(
    image_path: str,
    text: str,
    output_path: str = None,
    font_size: int = 48,
    text_color: tuple = (255, 255, 255),
    position: str = "center",
    bg_color: tuple = (0, 0, 0, 160),
    padding: int = 30,
    max_width: int = 900,
) -> str:
    image_path = _validate_path(image_path, check_exists=True)
    text = text.strip()[:500]

    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_text{ext}"
    else:
        output_path = _validate_path(output_path)

    img = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    line_height = font_size + 10
    total_height = len(lines) * line_height + padding * 2
    max_text_width = max(draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0] for line in lines)

    w, h = img.size
    box_w = max_text_width + padding * 2

    pos_map = {
        "center": ((w - box_w) // 2, (h - total_height) // 2),
        "top": ((w - box_w) // 2, 40),
        "bottom": ((w - box_w) // 2, h - total_height - 40),
    }
    x, y = pos_map.get(position, pos_map["center"])

    draw.rounded_rectangle(
        [x, y, x + box_w, y + total_height],
        radius=15,
        fill=bg_color,
    )

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        tx = x + (box_w - text_w) // 2
        ty = y + padding + i * line_height
        draw.text((tx, ty), line, fill=(*text_color, 255), font=font)

    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save(output_path, quality=95)

    print(f"Texto adicionado a imagem: {output_path}")
    return output_path
