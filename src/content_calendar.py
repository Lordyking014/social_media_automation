import json
import os
from datetime import datetime, timedelta
from src.text_generator import _call_gemini


CALENDAR_FILE = "content_calendar.json"


def _load_calendar() -> dict:
    if os.path.exists(CALENDAR_FILE):
        with open(CALENDAR_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"posts": []}


def _save_calendar(calendar: dict):
    with open(CALENDAR_FILE, "w", encoding="utf-8") as f:
        json.dump(calendar, f, indent=2, ensure_ascii=False)


def generate_weekly_plan(niche: str, days: int = 7) -> dict:
    prompt = f"""Crie um plano de conteudo para {days} dias no nicho: {niche}

Para cada dia, defina:
- TEMA: O tema do post
- FORMATO: feed, story, reel ou carrossel
- HORARIO: Melhor horario para postar
- LEGENDA_RESUMO: Resumo de 1 linha da legenda

Distribua variadamente entre feed, stories e reels.
Comece a partir de amana.

Formato:
DIA 1 (data): [dia da semana]
TEMA: [tema]
FORMATO: [tipo]
HORARIO: [horario]
LEGENDA_RESUMO: [resumo]

DIA 2 (data): ..."""

    response = _call_gemini(prompt)

    plan = {"niche": niche, "days": []}
    current_day = {}

    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("DIA"):
            if current_day:
                plan["days"].append(current_day)
            current_day = {"info": line, "theme": "", "format": "", "time": "", "summary": ""}
        elif line.startswith("TEMA:"):
            current_day["theme"] = line.replace("TEMA:", "").strip()
        elif line.startswith("FORMATO:"):
            current_day["format"] = line.replace("FORMATO:", "").strip()
        elif line.startswith("HORARIO:"):
            current_day["time"] = line.replace("HORARIO:", "").strip()
        elif line.startswith("LEGENDA_RESUMO:"):
            current_day["summary"] = line.replace("LEGENDA_RESUMO:", "").strip()

    if current_day:
        plan["days"].append(current_day)

    calendar = _load_calendar()
    calendar["posts"].extend(plan["days"])
    _save_calendar(calendar)

    print(f"\nPlano de conteudo para {niche}:")
    for day in plan["days"]:
        print(f"  {day['info']}: {day['theme']} ({day['format']}) as {day['time']}")

    return plan


def generate_monthly_plan(niche: str) -> dict:
    prompt = f"""Crie um plano mensal de conteudo para Instagram no nicho: {niche}

Semanas 1-4, com 4 posts por semana (Seg, Qua, Sex, Dom).

Para cada post:
TEMA: [tema]
FORMATO: [feed/story/reel/carrossel]
HORARIO: [horario sugerido]

Total: 16 posts

Formato:
SEMANA 1:
- Segunda: TEMA: [tema] | FORMATO: [tipo] | HORARIO: [hora]
- Quarta: ...
- Sexta: ...
- Domingo: ...

SEMANA 2: ..."""

    response = _call_gemini(prompt)

    plan = {"niche": niche, "type": "monthly", "content": response}

    calendar = _load_calendar()
    calendar["monthly_plan"] = plan
    _save_calendar(calendar)

    print(f"\nPlano mensal gerado para {niche}")
    print(response)

    return plan


def list_calendar() -> dict:
    return _load_calendar()


def clear_calendar():
    _save_calendar({"posts": []})
    print("Calendario limpo.")
