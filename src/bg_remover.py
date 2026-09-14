import os
from PIL import Image
import numpy as np


def _validate_path(path: str, check_exists: bool = False) -> str:
    path = os.path.normpath(path)
    if ".." in path:
        raise ValueError(f"Caminho invalido: {path}")
    if check_exists and not os.path.exists(path):
        raise ValueError(f"Arquivo nao existe: {path}")
    return path


def remove_background_simple(image_path: str, output_path: str = None, threshold: int = 240) -> str:
    image_path = _validate_path(image_path, check_exists=True)

    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_nobg{ext}"
    else:
        output_path = _validate_path(output_path)

    threshold = max(0, min(255, threshold))

    img = Image.open(image_path).convert("RGBA")
    data = np.array(img)

    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]

    white_mask = (r > threshold) & (g > threshold) & (b > threshold)
    data[white_mask] = [255, 255, 255, 0]

    result = Image.fromarray(data)
    result.save(output_path, "PNG")

    print(f"Fundo removido: {output_path}")
    return output_path


def change_background(
    image_path: str,
    background_color: tuple = (255, 255, 255),
    output_path: str = None,
) -> str:
    image_path = _validate_path(image_path, check_exists=True)

    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_newbg{ext}"
    else:
        output_path = _validate_path(output_path)

    background_color = tuple(max(0, min(255, c)) for c in background_color[:3])

    img = Image.open(image_path).convert("RGBA")
    data = np.array(img)

    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]

    transparent_mask = a == 0

    bg = Image.new("RGBA", img.size, (*background_color, 255))
    bg_data = np.array(bg)

    bg_data[~transparent_mask] = data[~transparent_mask]

    result = Image.fromarray(bg_data)
    result.convert("RGB").save(output_path, quality=95)

    print(f"Fundo alterado: {output_path}")
    return output_path


def create_gradient_bg(
    width: int = 1080,
    height: int = 1080,
    color1: tuple = (131, 58, 180),
    color2: tuple = (253, 29, 29),
    output_path: str = "gradient_bg.png",
) -> str:
    output_path = _validate_path(output_path)

    width = max(100, min(4096, width))
    height = max(100, min(4096, height))

    img = Image.new("RGB", (width, height))
    pixels = img.load()

    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        for x in range(width):
            pixels[x, y] = (r, g, b)

    img.save(output_path, quality=95)
    print(f"Gradiente gerado: {output_path}")
    return output_path
