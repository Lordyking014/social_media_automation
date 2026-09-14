import json
import os
from datetime import datetime, timedelta


SCHEDULE_FILE = "schedule.json"


def _load_schedule() -> list:
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_schedule(schedule: list):
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(schedule, f, indent=2, ensure_ascii=False)


def schedule_post(
    topic: str,
    platforms: list[str],
    scheduled_time: str,
    tone: str = "profissional",
) -> dict:
    schedule = _load_schedule()

    post = {
        "id": len(schedule) + 1,
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
        if post["status"] == "pending":
            post_time = datetime.fromisoformat(post["scheduled_time"])
            if post_time <= now:
                pending.append(post)

    return pending


def mark_as_done(post_id: int):
    schedule = _load_schedule()
    for post in schedule:
        if post["id"] == post_id:
            post["status"] = "done"
            post["published_at"] = datetime.now().isoformat()
            break
    _save_schedule(schedule)


def listScheduled_posts() -> list:
    schedule = _load_schedule()
    return [p for p in schedule if p["status"] == "pending"]


def cancel_post(post_id: int) -> bool:
    schedule = _load_schedule()
    for post in schedule:
        if post["id"] == post_id and post["status"] == "pending":
            post["status"] = "cancelled"
            _save_schedule(schedule)
            print(f"Post {post_id} cancelado.")
            return True
    print(f"Post {post_id} nao encontrado ou ja executado.")
    return False
