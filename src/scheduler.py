import json
import os
import uuid
from datetime import datetime


SCHEDULE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SCHEDULE_FILE = os.path.join(SCHEDULE_DIR, "schedule.json")


def _ensure_dir():
    os.makedirs(SCHEDULE_DIR, exist_ok=True)


def _load_schedule() -> list:
    _ensure_dir()
    if os.path.exists(SCHEDULE_FILE):
        try:
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    return []
                return data
        except (json.JSONDecodeError, ValueError):
            return []
    return []


def _save_schedule(schedule: list):
    _ensure_dir()
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(schedule, f, indent=2, ensure_ascii=False)


def schedule_post(
    topic: str,
    platforms: list[str],
    scheduled_time: str,
    tone: str = "profissional",
) -> dict:
    topic = topic.strip()[:200]
    tone = tone.strip()[:50]

    try:
        datetime.fromisoformat(scheduled_time)
    except ValueError:
        raise ValueError(f"Formato de data invalido: {scheduled_time}. Use YYYY-MM-DD HH:MM")

    valid_platforms = {"instagram", "facebook", "tiktok", "twitter"}
    platforms = [p for p in platforms if p in valid_platforms]
    if not platforms:
        raise ValueError("Nenhuma plataforma valida selecionada")

    schedule = _load_schedule()

    post = {
        "id": str(uuid.uuid4())[:8],
        "topic": topic,
        "platforms": platforms,
        "tone": tone,
        "scheduled_time": scheduled_time,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }

    schedule.append(post)
    _save_schedule(schedule)
    print(f"Post agendado: {scheduled_time} | Topico: {topic}")
    return post


def get_pending_posts() -> list:
    schedule = _load_schedule()
    now = datetime.now()
    pending = []

    for post in schedule:
        if post.get("status") == "pending":
            try:
                post_time = datetime.fromisoformat(post["scheduled_time"])
                if post_time <= now:
                    pending.append(post)
            except (ValueError, KeyError):
                continue

    return pending


def mark_as_done(post_id: str):
    schedule = _load_schedule()
    for post in schedule:
        if post.get("id") == post_id:
            post["status"] = "done"
            post["published_at"] = datetime.now().isoformat()
            break
    _save_schedule(schedule)


def listScheduled_posts() -> list:
    schedule = _load_schedule()
    return [p for p in schedule if p.get("status") == "pending"]


def cancel_post(post_id: str) -> bool:
    schedule = _load_schedule()
    for post in schedule:
        if post.get("id") == post_id and post.get("status") == "pending":
            post["status"] = "cancelled"
            _save_schedule(schedule)
            print(f"Post {post_id} cancelado.")
            return True
    print(f"Post {post_id} nao encontrado ou ja executado.")
    return False
