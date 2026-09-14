from src.text_generator import _call_gemini


def generate_variants(topic: str, num_variants: int = 3, tone: str = "profissional") -> list:
    prompt = f"""Crie {num_variants} versoes diferentes de legenda para Instagram sobre: {topic}

Tom de voz: {tone}
Cada variante deve ter um estilo diferente:
- Variante 1: Storytelling (contar uma historia)
- Variante 2: Lista/Dicas (.lista pratica)
- Variante 3: Pergunta/Engajamento (incentivar comentarios)

Formato para cada variante:
VARIANTE [numero] (ESTILO: [tipo]):
[legenda completa com hashtags]

Seja criativo e cada variante deve ser unica."""

    response = _call_gemini(prompt)

    variants = []
    current = {}

    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("VARIANTE"):
            if current:
                variants.append(current)
            parts = line.split("(")
            num = parts[0].replace("VARIANTE", "").strip()
            style = parts[1].replace("ESTILO:", "").replace("):", "").strip() if len(parts) > 1 else ""
            current = {"number": num, "style": style, "caption": ""}
        elif current and line:
            current["caption"] += line + "\n"

    if current:
        variants.append(current)

    print(f"\n{len(variants)} variantes geradas:")
    for v in variants:
        print(f"\n--- Variante {v['number']} ({v['style']}) ---")
        print(v["caption"].strip())

    return variants


def compare_captions(caption_a: str, caption_b: str) -> dict:
    prompt = f"""Compare essas 2 legendas de Instagram e diga qual e melhor:

LEGENDA A:
{caption_a}

LEGENDA B:
{caption_b}

Analise:
1. Engajamento (qual incentiva mais comentarios?)
2. Clareza (qual transmite melhor a mensagem?)
3. CTA (qual tem chamada para acao mais forte?)
4. Formatacao (qual usa melhor emojis e espacamento?)
5. Hashtags (qual tem hashtags mais estrategicas?)

Resultado:
VENCEDORA: [A ou B]
NOTA_A: [1-10]
NOTA_B: [1-10]
MOTIVO: [explicacao resumida]
DICA_MELHORIA: [sugestao para melhorar a perdedora]"""

    response = _call_gemini(prompt)

    result = {"raw": response}
    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("VENCEDORA:"):
            result["winner"] = line.replace("VENCEDORA:", "").strip()
        elif line.startswith("NOTA_A:"):
            result["score_a"] = line.replace("NOTA_A:", "").strip()
        elif line.startswith("NOTA_B:"):
            result["score_b"] = line.replace("NOTA_B:", "").strip()
        elif line.startswith("MOTIVO:"):
            result["reason"] = line.replace("MOTIVO:", "").strip()

    print(f"\nResultado A/B Test:")
    print(f"  Vencedora: {result.get('winner', 'N/A')}")
    print(f"  Nota A: {result.get('score_a', 'N/A')}")
    print(f"  Nota B: {result.get('score_b', 'N/A')}")
    print(f"  Motivo: {result.get('reason', 'N/A')}")

    return result
