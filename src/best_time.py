from datetime import datetime


BEST_TIMES = {
    "instagram": {
        "segunda": {"manha": "07:00-09:00", "almoco": "11:00-13:00", "noite": "19:00-21:00"},
        "terca": {"manha": "07:00-09:00", "almoco": "11:00-13:00", "noite": "19:00-21:00"},
        "quarta": {"manha": "07:00-09:00", "almoco": "12:00-14:00", "noite": "19:00-21:00"},
        "quinta": {"manha": "07:00-09:00", "almoco": "11:00-13:00", "noite": "18:00-20:00"},
        "sexta": {"manha": "07:00-09:00", "almoco": "11:00-13:00", "noite": "17:00-19:00"},
        "sabado": {"manha": "09:00-11:00", "almoco": "12:00-14:00", "noite": "19:00-21:00"},
        "domingo": {"manha": "10:00-12:00", "almoco": "13:00-15:00", "noite": "19:00-21:00"},
    },
    "facebook": {
        "segunda": {"manha": "09:00-11:00", "almoco": "13:00-15:00", "noite": "18:00-20:00"},
        "terca": {"manha": "09:00-11:00", "almoco": "13:00-15:00", "noite": "18:00-20:00"},
        "quarta": {"manha": "09:00-11:00", "almoco": "12:00-14:00", "noite": "18:00-20:00"},
        "quinta": {"manha": "09:00-11:00", "almoco": "13:00-15:00", "noite": "17:00-19:00"},
        "sexta": {"manha": "09:00-11:00", "almoco": "13:00-15:00", "noite": "16:00-18:00"},
        "sabado": {"manha": "10:00-12:00", "almoco": "13:00-15:00", "noite": "18:00-20:00"},
        "domingo": {"manha": "11:00-13:00", "almoco": "14:00-16:00", "noite": "19:00-21:00"},
    },
}


def get_best_times(platform: str = "instagram") -> dict:
    days_pt = {
        0: "segunda", 1: "terca", 2: "quarta",
        3: "quinta", 4: "sexta", 5: "sabado", 6: "domingo",
    }

    now = datetime.now()
    today = days_pt[now.weekday()]
    tomorrow_idx = (now.weekday() + 1) % 7
    tomorrow = days_pt[tomorrow_idx]

    platform_times = BEST_TIMES.get(platform, BEST_TIMES["instagram"])

    result = {
        "platform": platform,
        "hoje": {"dia": today, "horarios": platform_times.get(today, {})},
        "amanha": {"dia": tomorrow, "horarios": platform_times.get(tomorrow, {})},
    }

    print(f"\nMelhores horarios para {platform}:")
    print(f"  Hoje ({today}):")
    for periodo, horario in platform_times.get(today, {}).items():
        print(f"    {periodo}: {horario}")
    print(f"  Amanha ({tomorrow}):")
    for periodo, horario in platform_times.get(tomorrow, {}).items():
        print(f"    {periodo}: {horario}")

    return result


def suggest_next_post_time(platform: str = "instagram") -> str:
    days_pt = {
        0: "segunda", 1: "terca", 2: "quarta",
        3: "quinta", 4: "sexta", 5: "sabado", 6: "domingo",
    }

    now = datetime.now()
    today = days_pt[now.weekday()]
    current_hour = now.hour

    platform_times = BEST_TIMES.get(platform, BEST_TIMES["instagram"])
    today_times = platform_times.get(today, {})

    for periodo, horario in today_times.items():
        start, end = horario.split("-")
        start_hour = int(start.split(":")[0])
        end_hour = int(end.split(":")[0])

        if start_hour > current_hour:
            return f"{horario} (hoje, {periodo})"

    tomorrow_idx = (now.weekday() + 1) % 7
    tomorrow = days_pt[tomorrow_idx]
    tomorrow_times = platform_times.get(tomorrow, {})

    first_period = list(tomorrow_times.values())[0] if tomorrow_times else "09:00-11:00"
    return f"{first_period} (amanha, {tomorrow})"
