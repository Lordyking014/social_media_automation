import requests
import config


GRAPH_API_URL = "https://graph.facebook.com/v18.0"


def create_media_container(image_path: str, caption: str) -> str:
    if not config.PLATFORMS["instagram"]["enabled"]:
        raise ValueError("Instagram nao configurado. Verifique o .env")

    token = config.PLATFORMS["instagram"]["token"]
    account_id = config.PLATFORMS["instagram"]["account_id"]

    with open(image_path, "rb") as image_file:
        response = requests.post(
            f"{GRAPH_API_URL}/{account_id}/media",
            data={
                "caption": caption,
                "access_token": token,
            },
            files={"image": image_file},
        )

    response.raise_for_status()
    return response.json()["id"]


def publish_media(media_id: str) -> dict:
    token = config.PLATFORMS["instagram"]["token"]
    account_id = config.PLATFORMS["instagram"]["account_id"]

    response = requests.post(
        f"{GRAPH_API_URL}/{account_id}/media_publish",
        data={
            "creation_id": media_id,
            "access_token": token,
        },
    )

    response.raise_for_status()
    return response.json()


def create_story_container(image_path: str) -> str:
    if not config.PLATFORMS["instagram"]["enabled"]:
        raise ValueError("Instagram nao configurado. Verifique o .env")

    token = config.PLATFORMS["instagram"]["token"]
    account_id = config.PLATFORMS["instagram"]["account_id"]

    with open(image_path, "rb") as image_file:
        response = requests.post(
            f"{GRAPH_API_URL}/{account_id}/media",
            data={
                "media_type": "STORIES",
                "access_token": token,
            },
            files={"image": image_file},
        )

    response.raise_for_status()
    return response.json()["id"]


def publish_story(media_id: str) -> dict:
    token = config.PLATFORMS["instagram"]["token"]
    account_id = config.PLATFORMS["instagram"]["account_id"]

    response = requests.post(
        f"{GRAPH_API_URL}/{account_id}/media_publish",
        data={
            "creation_id": media_id,
            "access_token": token,
        },
    )

    response.raise_for_status()
    return response.json()


def post_to_instagram(image_path: str, caption: str) -> dict:
    print("Publicando no Instagram (feed)...")
    media_id = create_media_container(image_path, caption)
    result = publish_media(media_id)
    print(f"Post publicado com sucesso! Media ID: {result.get('id')}")
    return result


def post_story_to_instagram(image_path: str) -> dict:
    print("Publicando nos Stories do Instagram...")
    media_id = create_story_container(image_path)
    result = publish_story(media_id)
    print(f"Story publicado com sucesso! Media ID: {result.get('id')}")
    return result
