import os
import sys
import time
import json
import signal
from datetime import datetime


PID_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "daemon.pid")
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "daemon.log")
CHECK_INTERVAL = 60


def _ensure_dir():
    os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)


def _log(message: str):
    _ensure_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())


def _save_pid(pid: int):
    _ensure_dir()
    with open(PID_FILE, "w") as f:
        f.write(str(pid))


def _load_pid() -> int:
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0


def _remove_pid():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)


def _is_running() -> bool:
    pid = _load_pid()
    if pid == 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        _remove_pid()
        return False


def _process_scheduled_posts():
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from src.scheduler import get_pending_posts, mark_as_done
    from src.text_generator import generate_feed_caption
    from src.image_generator import generate_image_from_topic
    from src.publishers.instagram import post_to_instagram, post_story_to_instagram
    from src.publishers.facebook import post_to_facebook
    from config import PLATFORMS

    pending = get_pending_posts()

    if not pending:
        return

    _log(f"Processando {len(pending)} posts pendentes...")

    for post in pending:
        try:
            _log(f"Post {post['id']}: {post['topic']}")

            caption = generate_feed_caption(post["topic"], post.get("tone", "profissional"))
            image_path = generate_image_from_topic(post["topic"])

            for platform in post.get("platforms", ["instagram"]):
                if not PLATFORMS.get(platform, {}).get("enabled"):
                    _log(f"  {platform}: nao configurado, pulando")
                    continue

                try:
                    if platform == "instagram":
                        post_to_instagram(image_path, caption)
                        post_story_to_instagram(image_path)
                    elif platform == "facebook":
                        post_to_facebook(image_path, caption)
                    _log(f"  {platform}: publicado com sucesso")
                except Exception as e:
                    _log(f"  {platform}: erro - {e}")

            mark_as_done(post["id"])
            _log(f"Post {post['id']} concluido")

        except Exception as e:
            _log(f"Erro no post {post.get('id', '?')}: {e}")


def _daemon_loop():
    _log("Servico iniciado")
    _log(f"Verificando posts a cada {CHECK_INTERVAL} segundos")

    while True:
        try:
            _process_scheduled_posts()
        except Exception as e:
            _log(f"Erro no ciclo: {e}")

        time.sleep(CHECK_INTERVAL)


def start_daemon():
    if _is_running():
        pid = _load_pid()
        print(f"Servico ja esta rodando (PID: {pid})")
        return

    pid = os.getpid()
    _save_pid(pid)

    _log(f"Servico iniciado (PID: {pid})")

    signal.signal(signal.SIGTERM, lambda s, f: stop_daemon())
    signal.signal(signal.SIGINT, lambda s, f: stop_daemon())

    _daemon_loop()


def stop_daemon():
    pid = _load_pid()
    if pid == 0:
        print("Servico nao esta rodando")
        return

    try:
        os.kill(pid, signal.SIGTERM)
        _log(f"Servico parado (PID: {pid})")
    except OSError:
        _log("Servico nao estava rodando")

    _remove_pid()


def daemon_status():
    if _is_running():
        pid = _load_pid()
        print(f"Servico rodando (PID: {pid})")

        if os.path.exists(LOG_FILE):
            print("\nUltimas 10 linhas do log:")
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[-10:]:
                    print(f"  {line.strip()}")
    else:
        print("Servico parado")


def run_once():
    _log("Executando uma vez...")
    _process_scheduled_posts()
    _log("Concluido")
