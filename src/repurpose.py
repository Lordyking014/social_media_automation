from src.text_generator import _call_gemini
from src.image_generator import generate_image


def repurpose_content(topic: str, original_caption: str = None) -> dict:
    if not original_caption:
        original_caption = _call_gemini(f"Escreva uma legenda curta sobre: {topic}")

    prompt = f"""Reaproveite este conteudo para criar 4 formatos diferentes:

CONTEUDO ORIGINAL:
{original_caption}

Crie:
1. STORY_TEXT: Texto curto para 3 stories (max 120 chars cada)
2. REEL_HOOK: Gancho de 3 segundos para Reels
3. THREAD: 3 tweets para Twitter/Thread
4. CAROUSEL_TITLES: 5 titulos para carrossel

Formato:
STORY_1: [texto]
STORY_2: [texto]
STORY_3: [texto]
REEL_HOOK: [texto]
TWEET_1: [texto]
TWEET_2: [texto]
TWEET_3: [texto]
CAROUSEL_1: [titulo]
CAROUSEL_2: [titulo]
CAROUSEL_3: [titulo]
CAROUSEL_4: [titulo]
CAROUSEL_5: [titulo]"""

    response = _call_gemini(prompt)

    result = {"topic": topic, "original": original_caption, "formats": {}}

    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("STORY_1:"):
            result["formats"]["story_1"] = line.replace("STORY_1:", "").strip()
        elif line.startswith("STORY_2:"):
            result["formats"]["story_2"] = line.replace("STORY_2:", "").strip()
        elif line.startswith("STORY_3:"):
            result["formats"]["story_3"] = line.replace("STORY_3:", "").strip()
        elif line.startswith("REEL_HOOK:"):
            result["formats"]["reel_hook"] = line.replace("REEL_HOOK:", "").strip()
        elif line.startswith("TWEET_1:"):
            result["formats"]["tweet_1"] = line.replace("TWEET_1:", "").strip()
        elif line.startswith("TWEET_2:"):
            result["formats"]["tweet_2"] = line.replace("TWEET_2:", "").strip()
        elif line.startswith("TWEET_3:"):
            result["formats"]["tweet_3"] = line.replace("TWEET_3:", "").strip()
        elif line.startswith("CAROUSEL_1:"):
            result["formats"]["carousel_1"] = line.replace("CAROUSEL_1:", "").strip()
        elif line.startswith("CAROUSEL_2:"):
            result["formats"]["carousel_2"] = line.replace("CAROUSEL_2:", "").strip()
        elif line.startswith("CAROUSEL_3:"):
            result["formats"]["carousel_3"] = line.replace("CAROUSEL_3:", "").strip()
        elif line.startswith("CAROUSEL_4:"):
            result["formats"]["carousel_4"] = line.replace("CAROUSEL_4:", "").strip()
        elif line.startswith("CAROUSEL_5:"):
            result["formats"]["carousel_5"] = line.replace("CAROUSEL_5:", "").strip()

    print(f"\nConteudo reaproveitado para '{topic}':")
    for key, value in result["formats"].items():
        print(f"  {key}: {value}")

    return result


def generate_multi_format(topic: str, output_dir: str = "repurposed") -> dict:
    import os
    os.makedirs(output_dir, exist_ok=True)

    repurposed = repurpose_content(topic)

    images = {}
    formats_to_image = {
        "feed": "A professional Instagram feed post about {topic}, modern design, vibrant colors",
        "story": "A vertical Instagram story design about {topic}, bold text area, engaging",
        "reel_cover": "A YouTube thumbnail style cover for a Reel about {topic}, eye-catching",
    }

    for fmt, prompt_template in formats_to_image.items():
        path = os.path.join(output_dir, f"{fmt}.png")
        generate_image(prompt_template.format(topic=topic), path)
        images[fmt] = path

    repurposed["images"] = images
    print(f"\nImagens geradas em '{output_dir}/'")
    return repurposed
