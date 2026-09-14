import os
from src.text_generator import generate_feed_caption, generate_story_text
from src.image_generator import generate_image_from_topic
from src.branding import add_watermark


def generate_batch(topics: list[str], watermark: str = None, output_dir: str = "batch") -> dict:
    os.makedirs(output_dir, exist_ok=True)

    results = {"posts": []}

    for i, topic in enumerate(topics):
        print(f"\n{'='*40}")
        print(f"POST {i+1}/{len(topics)}: {topic}")
        print(f"{'='*40}")

        print("  Gerando legenda...")
        caption = generate_feed_caption(topic)

        print("  Gerando stories...")
        stories = generate_story_text(topic)

        print("  Gerando imagem...")
        image_path = generate_image_from_topic(topic, os.path.join(output_dir, f"post_{i+1}.png"))

        if watermark:
            image_path = add_watermark(image_path, text=watermark, output_path=os.path.join(output_dir, f"post_{i+1}_wm.png"))

        post = {
            "topic": topic,
            "caption": caption,
            "stories": stories,
            "image": image_path,
        }
        results["posts"].append(post)

        print(f"  Post {i+1} pronto!")

    results["total"] = len(results["posts"])
    results["output_dir"] = output_dir

    print(f"\n{'='*40}")
    print(f"LOTE COMPLETO: {len(results['posts'])} posts em '{output_dir}/'")
    print(f"{'='*40}")

    return results


def generate_week_batch(niche: str, watermark: str = None) -> dict:
    from src.text_generator import _call_gemini

    prompt = f"""Sugira 7 temas de posts para Instagram no nicho: {niche}
Um para cada dia da semana.

Formato:
1. [tema]
2. [tema]
3. [tema]
4. [tema]
5. [tema]
6. [tema]
7. [tema]"""

    response = _call_gemini(prompt)

    topics = []
    for line in response.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            topic = line.split(".", 1)[1].strip() if "." in line else line
            topics.append(topic)

    print(f"Temas gerados para {niche}:")
    for i, t in enumerate(topics, 1):
        print(f"  {i}. {t}")

    return generate_batch(topics, watermark=watermark)
