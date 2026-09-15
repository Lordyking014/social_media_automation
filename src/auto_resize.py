import os
from PIL import Image


PLATFORM_SIZES = {
    "instagram_feed": {"width": 1080, "height": 1080, "name": "Instagram Feed"},
    "instagram_story": {"width": 1080, "height": 1920, "name": "Instagram Story"},
    "instagram_reel": {"width": 1080, "height": 1920, "name": "Instagram Reel"},
    "instagram_carousel": {"width": 1080, "height": 1350, "name": "Instagram Carrossel"},
    "facebook_post": {"width": 1200, "height": 630, "name": "Facebook Post"},
    "facebook_story": {"width": 1080, "height": 1920, "name": "Facebook Story"},
    "twitter_post": {"width": 1200, "height": 675, "name": "Twitter/X Post"},
    "linkedin_post": {"width": 1200, "height": 627, "name": "LinkedIn Post"},
    "pinterest_pin": {"width": 1000, "height": 1500, "name": "Pinterest Pin"},
    "youtube_thumb": {"width": 1280, "height": 720, "name": "YouTube Thumbnail"},
    "youtube_banner": {"width": 2560, "height": 1440, "name": "YouTube Banner"},
    "tiktok": {"width": 1080, "height": 1920, "name": "TikTok"},
}


def _validate_path(path: str) -> str:
    path = os.path.normpath(path)
    if ".." in path:
        raise ValueError(f"Caminho invalido: {path}")
    return path


def resize_image(image_path: str, platform: str, output_path: str = None) -> str:
    image_path = _validate_path(image_path)

    if platform not in PLATFORM_SIZES:
        raise ValueError(f"Plataforma '{platform}' nao encontrada. Opcoes: {', '.join(PLATFORM_SIZES.keys())}")

    target = PLATFORM_SIZES[platform]

    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_{platform}{ext}"
    else:
        output_path = _validate_path(output_path)

    img = Image.open(image_path)
    orig_w, orig_h = img.size

    target_ratio = target["width"] / target["height"]
    orig_ratio = orig_w / orig_h

    if orig_ratio > target_ratio:
        new_height = target["height"]
        new_width = int(new_height * orig_ratio)
    else:
        new_width = target["width"]
        new_height = int(new_width / orig_ratio)

    img_resized = img.resize((new_width, new_height), Image.LANCZOS)

    left = (new_width - target["width"]) // 2
    top = (new_height - target["height"]) // 2
    right = left + target["width"]
    bottom = top + target["height"]

    img_cropped = img_resized.crop((left, top, right, bottom))

    img_cropped.save(output_path, quality=95)

    print(f"Imagem redimensionada: {target['name']} ({target['width']}x{target['height']})")
    print(f"  Salva em: {output_path}")

    return output_path


def resize_for_all(image_path: str, platforms: list[str] = None) -> dict:
    if not platforms:
        platforms = ["instagram_feed", "instagram_story", "facebook_post", "twitter_post"]

    results = {}

    for platform in platforms:
        try:
            path = resize_image(image_path, platform)
            results[platform] = path
        except Exception as e:
            results[platform] = f"Erro: {e}"

    print(f"\nImagens geradas para {len(results)} plataformas:")
    for platform, path in results.items():
        print(f"  {PLATFORM_SIZES[platform]['name']}: {path}")

    return results


def get_platform_sizes() -> dict:
    print("\nTamanhos por plataforma:")
    for key, data in PLATFORM_SIZES.items():
        print(f"  {key}: {data['width']}x{data['height']} ({data['name']})")
    return PLATFORM_SIZES
