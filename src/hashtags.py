from src.text_generator import _call_gemini


def research_hashtags(topic: str, platform: str = "instagram", count: int = 15) -> list:
    prompt = f"""Pesquise e liste {count} hashtags relevantes para o tema: {topic}
Plataforma: {platform}

Regras:
- Hashtags populares e com boa buscabilidade
- Mix de hashtags grandes (1M+), medias (100k-1M) e nichadas (<100k)
- Em portugues brasileiro
- Formato: #hashtag

Retorne apenas a lista de hashtags, uma por linha, comecando com #"""

    response = _call_gemini(prompt)

    hashtags = []
    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("#") and len(line) > 1:
            hashtags.append(line)

    hashtags = hashtags[:count]

    print(f"\nHashtags sugeridas para {topic}:")
    for h in hashtags:
        print(f"  {h}")

    return hashtags


def get_hashtag_sets(topic: str) -> dict:
    prompt = f"""Para o tema "{topic}", crie 3 conjuntos de hashtags para Instagram:

CONJUNTO_1 (Populares - alcance maximo): 5 hashtags com mais de 1M de posts
CONJUNTO_2 (Medias - equilibrio): 5 hashtags entre 100k e 1M de posts
CONJUNTO_3 (Nichadas - engajamento): 5 hashtags com menos de 100k de posts

Formato exato:
CONJUNTO_1: #tag1 #tag2 #tag3 #tag4 #tag5
CONJUNTO_2: #tag1 #tag2 #tag3 #tag4 #tag5
CONJUNTO_3: #tag1 #tag2 #tag3 #tag4 #tag5"""

    response = _call_gemini(prompt)

    result = {}
    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("CONJUNTO_1:"):
            result["populares"] = line.replace("CONJUNTO_1:", "").strip().split()
        elif line.startswith("CONJUNTO_2:"):
            result["medias"] = line.replace("CONJUNTO_2:", "").strip().split()
        elif line.startswith("CONJUNTO_3:"):
            result["nichadas"] = line.replace("CONJUNTO_3:", "").strip().split()

    print(f"\nConjuntos de hashtags para '{topic}':")
    for tipo, tags in result.items():
        print(f"  {tipo}: {' '.join(tags)}")

    return result
