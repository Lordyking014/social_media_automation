import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")

FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")

PLATFORMS = {
    "instagram": {
        "enabled": bool(INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_BUSINESS_ACCOUNT_ID),
        "token": INSTAGRAM_ACCESS_TOKEN,
        "account_id": INSTAGRAM_BUSINESS_ACCOUNT_ID,
    },
    "facebook": {
        "enabled": bool(FACEBOOK_ACCESS_TOKEN and FACEBOOK_PAGE_ID),
        "token": FACEBOOK_ACCESS_TOKEN,
        "page_id": FACEBOOK_PAGE_ID,
    },
}
