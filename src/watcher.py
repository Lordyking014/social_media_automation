import os
import time
import json
from datetime import datetime


WATCH_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "inbox")
PROCESSED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "processed")


def _ensure_dirs():
    os.makedirs(WATCH_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def _process_file(filepath: str):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from src.text_generator import generate_feed_caption, generate_story_text
    from src.image_generator import generate_image_from_topic

    filename = os.path.basename(filepath)
    print(f"Processando: {filename}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        return

    lines = content.split("\n")
    topic = lines[0].strip()
    tone = lines[1].strip() if len(lines) > 1 else "profissional"
    platforms = lines[2].strip().split(",") if len(lines) > 2 else ["instagram"]

    print(f"Topico: {topic}")
    print(f"Tom: {tone}")
    print(f"Plataformas: {platforms}")

    caption = generate_feed_caption(topic, tone)
    stories = generate_story_text(topic, tone)
    image_path = generate_image_from_topic(topic)

    result = {
        "topic": topic,
        "tone": tone,
        "platforms": platforms,
        "caption": caption,
        "stories": stories,
        "image": image_path,
        "processed_at": datetime.now().isoformat(),
    }

    output_file = os.path.join(PROCESSED_DIR, f"{filename}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    processed_file = os.path.join(PROCESSED_DIR, filename)
    os.rename(filepath, processed_file)

    print(f"Concluido: {output_file}")


def watch_folder():
    _ensure_dirs()

    print(f"Monitorando pasta: {WATCH_DIR}")
    print("Para criar um post, crie um arquivo .txt na pasta 'inbox/'")
    print("Formato do arquivo:")
    print("  Linha 1: Topico/tema")
    print("  Linha 2: Tom (opcional: profissional, casual, etc)")
    print("  Linha 3: Plataformas separadas por virgula (opcional)")
    print("\nPressione Ctrl+C para parar\n")

    processed = set()

    while True:
        try:
            for filename in os.listdir(WATCH_DIR):
                if filename.endswith(".txt") and filename not in processed:
                    filepath = os.path.join(WATCH_DIR, filename)
                    try:
                        _process_file(filepath)
                        processed.add(filename)
                    except Exception as e:
                        print(f"Erro ao processar {filename}: {e}")
        except Exception as e:
            print(f"Erro no monitor: {e}")

        time.sleep(5)
