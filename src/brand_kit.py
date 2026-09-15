import json
import os


BRAND_KIT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "brand_kit.json")


def _ensure_dir():
    os.makedirs(os.path.dirname(BRAND_KIT_FILE), exist_ok=True)


def _load_brand() -> dict:
    _ensure_dir()
    if os.path.exists(BRAND_KIT_FILE):
        try:
            with open(BRAND_KIT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}


def _save_brand(brand: dict):
    _ensure_dir()
    with open(BRAND_KIT_FILE, "w", encoding="utf-8") as f:
        json.dump(brand, f, indent=2, ensure_ascii=False)


def create_brand(
    name: str,
    colors: dict = None,
    fonts: dict = None,
    tone: str = "profissional",
    hashtags: list = None,
    bio: str = "",
) -> dict:
    brand = {
        "name": name,
        "colors": colors or {"primary": "#000000", "secondary": "#FFFFFF", "accent": "#FF0000"},
        "fonts": fonts or {"heading": "Arial", "body": "Arial", "size": "16px"},
        "tone": tone,
        "hashtags": hashtags or [],
        "bio": bio,
        "created_at": __import__("datetime").datetime.now().isoformat(),
    }

    _save_brand(brand)
    print(f"Kit de marca '{name}' criado!")
    return brand


def get_brand() -> dict:
    brand = _load_brand()
    if not brand:
        print("Nenhum kit de marca configurado. Use: main.py brand create")
        return {}

    print(f"\nKit de Marca: {brand.get('name', 'N/A')}")
    print(f"  Tom: {brand.get('tone', 'N/A')}")
    print(f"  Cores: {brand.get('colors', {})}")
    print(f"  Fontes: {brand.get('fonts', {})}")
    print(f"  Hashtags: {brand.get('hashtags', [])}")
    print(f"  Bio: {brand.get('bio', 'N/A')}")

    return brand


def update_brand(**kwargs) -> dict:
    brand = _load_brand()
    if not brand:
        print("Crie um kit de marca primeiro: main.py brand create")
        return {}

    for key, value in kwargs.items():
        if value is not None:
            brand[key] = value

    _save_brand(brand)
    print(f"Kit de marca atualizado!")
    return brand


def delete_brand():
    if os.path.exists(BRAND_KIT_FILE):
        os.remove(BRAND_KIT_FILE)
        print("Kit de marca removido!")
    else:
        print("Nenhum kit de marca para remover.")


def apply_brand(caption: str) -> str:
    brand = _load_brand()
    if not brand:
        return caption

    tone = brand.get("tone", "profissional")
    hashtags = brand.get("hashtags", [])

    if hashtags and not any(h.startswith("#") for h in caption.split() if h.startswith("#")):
        hashtag_str = " ".join(hashtags[:5])
        caption = f"{caption}\n\n{hashtag_str}"

    print(f"Marca '{brand.get('name')}' aplicada (tom: {tone})")
    return caption
