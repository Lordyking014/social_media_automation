from src.text_generator import _call_gemini, _sanitize_input


def generate_youtube_script(topic: str, duration: int = 10, tone: str = "educativo") -> dict:
    topic = _sanitize_input(topic)

    prompt = f"""Crie um roteiro completo para video YouTube sobre: {topic}

Duracao: {duration} minutos
Tom: {tone}

Estrutura:
1. INTRO (0:00-0:30): Gancho + apresentacao do tema
2. DESENVOLVIMENTO (minutos 1-{duration-1}): Conteudo principal em secoes
3. CONCLUSAO (ultimo minuto): Resumo + CTA + proximo video

Para cada secao inclua:
- TEMPO: [tempo]
- TITULO: [titulo da secao]
- CONTEUDO: [o que falar]
- VISUAL: [oque mostrar na tela]

Formato:
INTRO:
TEMPO: 0:00-0:30
TITULO: [titulo]
CONTEUDO: [conteudo]
VISUAL: [visual]

SECAO_1:
TEMPO: [tempo]
TITULO: [titulo]
CONTEUDO: [conteudo]
VISUAL: [visual]

..."""

    response = _call_gemini(prompt)

    result = {
        "topic": topic,
        "duration": duration,
        "script": response,
    }

    print(f"\nRoteiro YouTube ({duration}min):")
    print(response)

    return result


def generate_podcast_script(topic: str, duration: int = 30, format_type: str = "monologo") -> dict:
    topic = _sanitize_input(topic)

    prompt = f"""Crie um roteiro de podcast sobre: {topic}

Duracao: {duration} minutos
Formato: {format_type} (monologo, entrevista, debate)

Estrutura:
1. ABERTURA: Musica + apresentacao
2. CONTEXTO: Por que esse tema importa
3. CONTEUDO: Pontos principais (3-5 topicos)
4. HISTORIAS: Exemplos praticos
5. ENCERRAMENTO: Resumo + CTA + proximo episodio

Para cada parte inclua:
- PARTE: [nome]
- DURACAO: [tempo estimado]
- TITULO: [titulo]
- PONTOS: [pontos principais]

Formato:
ABERTURA:
DURACAO: 2 min
TITULO: [titulo]
PONTOS: [pontos]

CONTEXTO:
DURACAO: 5 min
TITULO: [titulo]
PONTOS: [pontos]"""

    response = _call_gemini(prompt)

    result = {
        "topic": topic,
        "duration": duration,
        "format": format_type,
        "script": response,
    }

    print(f"\nRoteiro Podcast ({duration}min - {format_type}):")
    print(response)

    return result


def generate_tiktok_series(topic: str, num_videos: int = 5) -> dict:
    topic = _sanitize_input(topic)

    prompt = f"""Crie uma serie de {num_videos} videos curtos (TikTok/Reels) sobre: {topic}

Cada video deve ser:
- 15-60 segundos
- Ter gancho forte
- Ter Continua no proximo video
- Terminar com cliffhanger

Formato para cada video:
VIDEO_1:
GANCHO: [frase impactante]
DESENVOLVIMENTO: [conteudo curto]
CLIFFHANGER: [gancho para proximo]
LEGENDA: [legenda com hashtags]

VIDEO_2: ..."""

    response = _call_gemini(prompt)

    result = {
        "topic": topic,
        "num_videos": num_videos,
        "series": response,
    }

    print(f"\nSerie TikTok ({num_videos} videos):")
    print(response)

    return result


def generate_webinar_script(topic: str, duration: int = 60) -> dict:
    topic = _sanitize_input(topic)

    prompt = f"""Crie um roteiro de webinar sobre: {topic}

Duracao: {duration} minutos
Formato: Apresentacao + Q&A

Estrutura:
1. ABERTURA (5 min): Apresentacao + agenda
2. PROBLEMA (10 min): Por que importa
3. SOLUCAO (20 min): Conteudo principal
4. CASOS (10 min): Exemplos praticos
5. Q&A (10 min): Perguntas frequentes
6. ENCERRAMENTO (5 min): Resumo + oferta

Formato:
PARTE_1_ABERTURA:
TEMPO: 0-5 min
TOPICO: [topico]
TAREFAS: [tarefas]
SLIDES: [sugestoes de slides]"""

    response = _call_gemini(prompt)

    result = {
        "topic": topic,
        "duration": duration,
        "webinar": response,
    }

    print(f"\nRoteiro Webinar ({duration}min):")
    print(response)

    return result
