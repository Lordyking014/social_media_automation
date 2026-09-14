from src.text_generator import _call_gemini


def generate_poll(topic: str) -> dict:
    prompt = f"""Crie uma enquete para Instagram Stories sobre: {topic}

Formato:
PERGUNTA: [pergunta chamativa]
OPCAO_1: [opcao A]
OPCAO_2: [opcao B]
DICA: [dica de como usar a enquete]

Seja criativo e incentivoe votacao!"""

    response = _call_gemini(prompt)

    result = {"topic": topic, "type": "poll"}
    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("PERGUNTA:"):
            result["question"] = line.replace("PERGUNTA:", "").strip()
        elif line.startswith("OPCAO_1:"):
            result["option_a"] = line.replace("OPCAO_1:", "").strip()
        elif line.startswith("OPCAO_2:"):
            result["option_b"] = line.replace("OPCAO_2:", "").strip()
        elif line.startswith("DICA:"):
            result["tip"] = line.replace("DICA:", "").strip()

    print(f"\nEnquete para '{topic}':")
    print(f"  Pergunta: {result.get('question', '')}")
    print(f"  A: {result.get('option_a', '')}")
    print(f"  B: {result.get('option_b', '')}")

    return result


def generate_quiz(topic: str) -> dict:
    prompt = f"""Crie um quiz para Instagram Stories sobre: {topic}

Crie 3 perguntas com 3 alternativas cada.

Formato:
PERGUNTA_1: [pergunta]
A) [alternativa]
B) [alternativa]
C) [alternativa] (CORRETA)

PERGUNTA_2: ..."""

    response = _call_gemini(prompt)

    result = {"topic": topic, "type": "quiz", "questions": []}
    current_q = {}

    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("PERGUNTA_"):
            if current_q:
                result["questions"].append(current_q)
            current_q = {"question": line.split(":", 1)[1].strip(), "options": []}
        elif line.startswith(("A)", "B)", "C)")):
            current_q["options"].append(line)

    if current_q:
        result["questions"].append(current_q)

    print(f"\nQuiz para '{topic}':")
    for i, q in enumerate(result["questions"], 1):
        print(f"\n  Pergunta {i}: {q['question']}")
        for opt in q["options"]:
            print(f"    {opt}")

    return result


def generate_sliders(topic: str) -> dict:
    prompt = f"""Crie 3 sliders (barras de emoji) para Instagram Stories sobre: {topic}

Formato:
SLIDER_1: [pergunta] | EMOJI: [emoji]
SLIDER_2: [pergunta] | EMOJI: [emoji]
SLIDER_3: [pergunta] | EMOJI: [emoji]"""

    response = _call_gemini(prompt)

    result = {"topic": topic, "type": "sliders", "sliders": []}

    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("SLIDER_"):
            parts = line.split("|")
            question = parts[0].split(":", 1)[1].strip() if len(parts) > 0 else ""
            emoji = parts[1].split(":")[1].strip() if len(parts) > 1 else "😍"
            result["sliders"].append({"question": question, "emoji": emoji})

    print(f"\nSliders para '{topic}':")
    for s in result["sliders"]:
        print(f"  {s['emoji']} {s['question']}")

    return result


def generate_question_box(topic: str) -> dict:
    prompt = f"""Crie 3 perguntas para o box de perguntas do Instagram Stories sobre: {topic}

Formato:
PERGUNTA_1: [texto convidativo]
PERGUNTA_2: [texto convidativo]
PERGUNTA_3: [texto convidativo]

Seja curioso e incentivoe respostas!"""

    response = _call_gemini(prompt)

    result = {"topic": topic, "type": "question_box", "questions": []}

    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("PERGUNTA_"):
            result["questions"].append(line.split(":", 1)[1].strip())

    print(f"\nBox de perguntas para '{topic}':")
    for q in result["questions"]:
        print(f"  ❓ {q}")

    return result


def generate_emoji_slider(topic: str) -> dict:
    prompt = f"""Crie um slider de emoji criativo para Instagram Stories sobre: {topic}

Formato:
PERGUNTA: [pergunta engraçada]
EMOJI: [emoji representativo]
DICA: [como divulgar]"""

    response = _call_gemini(prompt)

    result = {"topic": topic, "type": "emoji_slider"}
    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("PERGUNTA:"):
            result["question"] = line.replace("PERGUNTA:", "").strip()
        elif line.startswith("EMOJI:"):
            result["emoji"] = line.replace("EMOJI:", "").strip()
        elif line.startswith("DICA:"):
            result["tip"] = line.replace("DICA:", "").strip()

    print(f"\nSlider de emoji para '{topic}':")
    print(f"  {result.get('emoji', '🔥')} {result.get('question', '')}")

    return result
