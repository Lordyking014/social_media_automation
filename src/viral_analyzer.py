from src.text_generator import _call_gemini, _sanitize_input


def analyze_viral_post(caption: str, engagement: str = "alto") -> dict:
    caption = _sanitize_input(caption, 2000)

    prompt = f"""Analise por que este post viralizou (engajamento: {engagement}):

POST:
{caption}

Analise:
1. GANCHO: O que prende atencao?
2. EMOCAO: Que emocao gera?
3. COMpartILHAMENTO: Por que compartilhariam?
4. COMENTARIO: O que leva a comentar?
5. SALVAMENTO: Por que salvam?
6. ESTRUTURA: Como esta organizado?
7. CTA: Qual a chamada para acao?
8. NOTAS: 1-10 para cada aspecto

Formato:
GANCHO: [analise] (nota: X/10)
EMOCAO: [analise] (nota: X/10)
COMPARTILHAMENTO: [analise] (nota: X/10)
COMENTARIO: [analise] (nota: X/10)
SALVAMENTO: [analise] (nota: X/10)
ESTRUTURA: [analise] (nota: X/10)
CTA: [analise] (nota: X/10)
NOTA_GERAL: X/10
SEGREDOS: [3 segredos do sucesso]
REPLICAR: [como replicar esse sucesso]"""

    response = _call_gemini(prompt)

    result = {
        "caption": caption,
        "engagement": engagement,
        "analysis": response,
    }

    print(f"\nAnalise viral:")
    print(response)

    return result


def suggest_viral_improvements(caption: str) -> dict:
    caption = _sanitize_input(caption, 2000)

    prompt = f"""Melhore este post para viralizar:

POST ATUAL:
{caption}

Sugira:
1. GANCHO_MELHORADO: 3 opcoes de gancho mais impactantes
2. ESTRUTURA: Como reorganizar para mais engajamento
3. CTA_MELHORADO: Chamadas mais fortes
4. HASHTAGS: Hashtags estrategicas
5. HORARIO: Melhor horario para postar
6. FORMATO: Sugerir formato alternativo (carrossel, reels, etc)

Formato:
GANCHO_1: [opcao 1]
GANCHO_2: [opcao 2]
GANCHO_3: [opcao 3]

ESTRUTURA_MELHORADA: [nova estrutura]
CTA_MELHORADO: [novas CTAs]
HASHTAGS: [hashtags]
HORARIO: [horario]
FORMATO: [formato sugerido]"""

    response = _call_gemini(prompt)

    result = {
        "original": caption,
        "improvements": response,
    }

    print(f"\nMelhorias virais:")
    print(response)

    return result


def generate_viral_hook(topic: str, num_hooks: int = 10) -> list:
    topic = _sanitize_input(topic)

    prompt = f"""Crie {num_hooks} ganchos virais para posts sobre: {topic}

Tipos de gancho:
1. Curiosidade
2. Polemico
3. Lista
4. Pergunta
5. Surpresa
6. Medo de perder (FOMO)
7. Historia
8. Dados/estatisticas
9. Antes/Depois
10. Desafio

Formato:
HOOK_1 (TIPO: [tipo]): [frase]
HOOK_2 (TIPO: [tipo]): [frase]
..."""

    response = _call_gemini(prompt)

    hooks = []
    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("HOOK_"):
            hooks.append(line)

    print(f"\n{len(hooks)} ganchos virais para '{topic}':")
    for h in hooks:
        print(f"  {h}")

    return hooks
