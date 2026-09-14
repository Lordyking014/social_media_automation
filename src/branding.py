from PIL import Image, ImageDraw, ImageFont
import os


def _validate_path(path: str, check_exists: bool = False) -> str:
    path = os.path.normpath(path)
    if ".." in path:
        raise ValueError(f"Caminho invalido: {path}")
    if check_exists and not os.path.exists(path):
        raise ValueError(f"Arquivo nao existe: {path}")
    return path


def add_watermark(
    image_path: str,
    text: str = "@seuperfil",
    output_path: str = None,
    opacity: int = 80,
    position: str = "bottom-right",
    font_size: int = 36,
) -> str:
    image_path = _validate_path(image_path, check_exists=True)
    text = text.strip()[:100]

    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_watermarked{ext}"
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

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = 20
    w, h = img.size

    positions = {
        "top-left": (padding, padding),
        "top-right": (w - text_width - padding, padding),
        "bottom-left": (padding, h - text_height - padding),
        "bottom-right": (w - text_width - padding, h - text_height - padding),
        "center": ((w - text_width) // 2, (h - text_height) // 2),
    }

    x, y = positions.get(position, positions["bottom-right"])

    draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)

    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save(output_path, quality=95)

    print(f"Marca d'agua adicionada: {output_path}")
    return output_path


def add_logo(
    image_path: str,
    logo_path: str,
    output_path: str = None,
    position: str = "bottom-right",
    logo_size: int = 80,
    padding: int = 20,
    opacity: int = 200,
) -> str:
    image_path = _validate_path(image_path, check_exists=True)
    logo_path = _validate_path(logo_path, check_exists=True)

    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_branded{ext}"
    else:
        output_path = _validate_path(output_path)

    img = Image.open(image_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    logo.thumbnail((logo_size, logo_size), Image.LANCZOS)

    if opacity < 255:
        alpha = logo.split()[3]
        alpha = alpha.point(lambda p: min(p, opacity))
        logo.putalpha(alpha)

    w, h = img.size
    lw, lh = logo.size

    positions = {
        "top-left": (padding, padding),
        "top-right": (w - lw - padding, padding),
        "bottom-left": (padding, h - lh - padding),
        "bottom-right": (w - lw - padding, h - lh - padding),
        "center": ((w - lw) // 2, (h - lh) // 2),
    }

    x, y = positions.get(position, positions["bottom-right"])

    img.paste(logo, (x, y), logo)
    img.convert("RGB").save(output_path, quality=95)

    print(f"Logo adicionado: {output_path}")
    return output_path
