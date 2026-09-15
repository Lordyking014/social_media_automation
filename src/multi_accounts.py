import json
import os


ACCOUNTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "accounts.json")


def _ensure_dir():
    os.makedirs(os.path.dirname(ACCOUNTS_FILE), exist_ok=True)


def _load_accounts() -> dict:
    _ensure_dir()
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {"accounts": [], "active": None}
    return {"accounts": [], "active": None}


def _save_accounts(data: dict):
    _ensure_dir()
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_account(name: str, username: str, platform: str = "instagram", bio: str = "") -> dict:
    data = _load_accounts()

    account = {
        "id": len(data["accounts"]) + 1,
        "name": name,
        "username": username,
        "platform": platform,
        "bio": bio,
        "posts": 0,
    }

    data["accounts"].append(account)

    if not data["active"]:
        data["active"] = account["id"]

    _save_accounts(data)
    print(f"Conta '{name}' (@{username}) adicionada!")
    return account


def list_accounts() -> list:
    data = _load_accounts()
    accounts = data.get("accounts", [])
    active_id = data.get("active")

    print("\nContas configuradas:")
    for acc in accounts:
        active = " [ATIVA]" if acc["id"] == active_id else ""
        print(f"  {acc['id']}. {acc['name']} (@{acc['username']}) - {acc['platform']}{active}")

    return accounts


def switch_account(account_id: int) -> bool:
    data = _load_accounts()

    for acc in data["accounts"]:
        if acc["id"] == account_id:
            data["active"] = account_id
            _save_accounts(data)
            print(f"Conta ativa: {acc['name']} (@{acc['username']})")
            return True

    print(f"Conta {account_id} nao encontrada")
    return False


def get_active_account() -> dict:
    data = _load_accounts()
    active_id = data.get("active")

    if not active_id:
        print("Nenhuma conta ativa. Use: main.py accounts list")
        return {}

    for acc in data["accounts"]:
        if acc["id"] == active_id:
            return acc

    return {}


def remove_account(account_id: int) -> bool:
    data = _load_accounts()

    for i, acc in enumerate(data["accounts"]):
        if acc["id"] == account_id:
            removed = data["accounts"].pop(i)
            if data["active"] == account_id:
                data["active"] = data["accounts"][0]["id"] if data["accounts"] else None
            _save_accounts(data)
            print(f"Conta '{removed['name']}' removida!")
            return True

    print(f"Conta {account_id} nao encontrada")
    return False


def get_account_stats() -> dict:
    data = _load_accounts()
    accounts = data.get("accounts", [])

    stats = {
        "total": len(accounts),
        "by_platform": {},
    }

    for acc in accounts:
        platform = acc.get("platform", "instagram")
        stats["by_platform"][platform] = stats["by_platform"].get(platform, 0) + 1

    print(f"\nEstatisticas:")
    print(f"  Total de contas: {stats['total']}")
    for platform, count in stats["by_platform"].items():
        print(f"  {platform}: {count}")

    return stats
