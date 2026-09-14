from src.text_generator import _call_gemini


NICHES = {
    "fitness": {
        "name": "Fitness/Saude",
        "hashtags": "#fitness #saude #treino #dieta #vidahealthy",
        "tones": ["motivacional", "educativo", "inspirador"],
    },
    "food": {
        "name": "Gastronomia",
        "hashtags": "#foodie #receita #culinaria #comida #foodporn",
        "tones": ["delicioso", "casual", "engajante"],
    },
    "tech": {
        "name": "Tecnologia",
        "hashtags": "#tecnologia #inovacao #futuro #digital #startup",
        "tones": ["informativo", "profissional", "inovador"],
    },
    "beauty": {
        "name": "Beleza",
        "hashtags": "#beleza #maquiagem #skincare #beauty #estetica",
        "tones": ["elegante", "amigavel", "expert"],
    },
    "business": {
        "name": "Negocios",
        "hashtags": "#negocios #empreendedorismo #sucesso #lideranca #vendas",
        "tones": ["profissional", "motivacional", "estrategico"],
    },
    "travel": {
        "name": "Viagem",
        "hashtags": "#viagem #turismo #aventura #travel #destino",
        "tones": ["aventureiro", "inspirador", "informativo"],
    },
    "education": {
        "name": "Educacao",
        "hashtags": "#educacao #aprendizado #estudos #conhecimento #escola",
        "tones": ["educativo", "motivacional", "claro"],
    },
    "fashion": {
        "name": "Moda",
        "hashtags": "#moda #fashion #estilo #tendencias #outfit",
        "tones": ["chic", "tendencia", "inspirador"],
    },
    "finance": {
        "name": "Financas",
        "hashtags": "#financas #investimentos #economia #dinheiro #rendafixa",
        "tones": ["informativo", "pratico", "confiavel"],
    },
    "realestate": {
        "name": "Imoveis",
        "hashtags": "#imoveis #casa #apartamento #investimentoimobiliario #moradia",
        "tones": ["profissional", "informativo", "confiavel"],
    },
}


def get_template(niche: str) -> dict:
    niche_data = NICHES.get(niche.lower())
    if not niche_data:
        print(f"Nicho '{niche}' nao encontrado. Disponiveis: {', '.join(NICHES.keys())}")
        return {}

    print(f"\nTemplate para nicho: {niche_data['name']}")
    print(f"  Hashtags: {niche_data['hashtags']}")
    print(f"  Tons: {', '.join(niche_data['tones'])}")

    return niche_data


def generate_niche_post(niche: str, topic: str = None, tone: str = None) -> dict:
    from src.text_generator import generate_feed_caption, generate_story_text

    niche_data = NICHES.get(niche.lower())
    if not niche_data:
        print(f"Nicho '{niche}' nao encontrado.")
        return {}

    if not topic:
        prompt = f"Sugira 1 tema trending para o nicho {niche_data['name']} no Instagram:"
        topic = _call_gemini(prompt).strip()

    if not tone:
        import random
        tone = random.choice(niche_data["tones"])

    print(f"\nGerando post para {niche_data['name']}: {topic}")

    caption = generate_feed_caption(topic, tone)
    stories = generate_story_text(topic, tone)

    result = {
        "niche": niche,
        "topic": topic,
        "tone": tone,
        "caption": caption,
        "stories": stories,
        "hashtags": niche_data["hashtags"],
    }

    print(f"\nLegenda gerada:")
    print(caption)

    return result


def list_niches():
    print("\nNichos disponiveis:")
    for key, data in NICHES.items():
        print(f"  {key}: {data['name']} | Tons: {', '.join(data['tones'])}")
