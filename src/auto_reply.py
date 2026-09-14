from src.text_generator import _call_gemini


def generate_reply(comment: str, tone: str = "amigavel", brand_voice: str = "") -> str:
    brand_context = f"Voz da marca: {brand_voice}" if brand_voice else ""

    prompt = f"""Gere uma resposta profissional e amigavel para este comentario:

COMENTARIO: {comment}
Tom: {tone}
{brand_context}

Regras:
- Seja genuino e personalizado
- Nao pareca robotico
- Incentore interacao
- Maximo 2 frases
- Use emoji com moderacao

Resposta:"""

    response = _call_gemini(prompt)
    return response.strip()


def generate_reply_set(comments: list[str], tone: str = "amigavel") -> list:
    results = []

    for comment in comments:
        reply = generate_reply(comment, tone)
        results.append({"comment": comment, "reply": reply})
        print(f"\nComentario: {comment}")
        print(f"Resposta: {reply}")

    return results


def classify_comment(comment: str) -> str:
    prompt = f"""Classifique este comentario em apenas UMA categoria:

COMENTARIO: {comment}

Categorias: POSITIVO | NEGATIVO | PERGUNTA | SPAM | INDIFERENTE

Responda apenas com a categoria:"""

    response = _call_gemini(prompt)
    return response.strip()


def generate_smart_replies(comments: list[str]) -> list:
    results = []

    for comment in comments:
        category = classify_comment(comment)

        tone_map = {
            "POSITIVO": "agradecido",
            "NEGATIVO": "empatico",
            "PERGUNTA": "informativo",
            "SPAM": "neutro",
            "INDIFERENTE": "amigavel",
        }

        reply = generate_reply(comment, tone=tone_map.get(category, "amigavel"))
        results.append({
            "comment": comment,
            "category": category,
            "reply": reply,
        })

        print(f"\n[{category}] {comment}")
        print(f"  -> {reply}")

    return results
