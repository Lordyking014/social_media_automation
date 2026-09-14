import requests
import config


GRAPH_API_URL = "https://graph.facebook.com/v18.0"


def post_to_facebook(image_path: str, message: str) -> dict:
    if not config.PLATFORMS["facebook"]["enabled"]:
        raise ValueError("Facebook nao configurado. Verifique o .env")

    token = config.PLATFORMS["facebook"]["token"]
    page_id = config.PLATFORMS["facebook"]["page_id"]

    print("Publicando no Facebook...")

    with open(image_path, "rb") as image_file:
        response = requests.post(
            f"{GRAPH_API_URL}/{page_id}/photos",
            data={
                "message": message,
                "access_token": token,
            },
            files={"source": image_file},
        )

    response.raise_for_status()
    result = response.json()
    print(f"Post publicado no Facebook com sucesso! Post ID: {result.get('id')}")
    return result
