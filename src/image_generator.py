import urllib.parse
import requests


def generate_image(prompt: str, output_path: str = "generated_image.png") -> str:
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"

    print(f"Gerando imagem com Pollinations.ai...")
    response = requests.get(url, timeout=120)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Imagem salva em: {output_path}")
    return output_path


def generate_image_from_topic(topic: str, output_path: str = "generated_image.png") -> str:
    from src.text_generator import generate_image_prompt

    prompt = generate_image_prompt(topic)
    print(f"Prompt gerado: {prompt}")

    return generate_image(prompt, output_path)
