import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Telegram bot config (use env vars or hardcode for testing)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Steam region
COUNTRY_CODE = 'DE'
STEAM_API_URL = (
    'https://api.steampowered.com/IPhysicalGoodsService/CheckInventoryAvailableByPackage/v1'
    '?origin=https:%2F%2Fstore.steampowered.com'
    f'&country_code={COUNTRY_CODE}&packageid='
)

# Deck versions to monitor
VERSIONS = [
    ("64", "903905", False),   # 64GB LCD
    ("256", "903906", False),  # 256GB LCD
    ("512", "903907", False),  # 512GB LCD
    ("512", "1202542", True),  # 512GB OLED
    ("1024", "1202547", True), # 1TB OLED
    ("Wasteland 2: Director's Cut", "240760", False), # Available game for testing
]

def send_telegram_message(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing BOT_TOKEN or CHAT_ID.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)
        if not response.ok:
            print("Failed to send Telegram message:", response.text)
    except Exception as e:
        print("Telegram error:", e)

def check_steam_deck(version: str, package_id: str, is_oled: bool):
    file_path = f"{package_id}.status"

    old_status = ""
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            old_status = f.read().strip()

    try:
        response = requests.get(STEAM_API_URL + package_id)
        data = response.json()
        new_status = str(data["response"]["inventory_available"])

        print(f"{datetime.now()} - {version}GB ({'OLED' if is_oled else 'LCD'}): {new_status}")

        # Update file
        with open(file_path, "w") as f:
            f.write(new_status)

        # Notify if status changed and product is now available
        if new_status != old_status and new_status == "True":
            send_telegram_message(
                f"🟢 Refurbished {version}GB {'OLED' if is_oled else 'LCD'} Steam Deck is now available!"
            )

    except Exception as e:
        print(f"Error checking version {version}: {e}")

def main():
    for version, package_id, is_oled in VERSIONS:
        check_steam_deck(version, package_id, is_oled)

if __name__ == "__main__":
    main()
