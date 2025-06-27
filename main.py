import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# ✅ Add your products here
PRODUCTS = {
    "Amul Buttermilk": "https://www.amazon.in/Amul-Protein-Buttermilk-protein-8x200mL/dp/B09RV8YWWT",
    # Add more:
    # "Amul Lassi": "https://www.amazon.in/example-product-url",
    # "Amul Milk": "https://www.amazon.in/example-milk-url"
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {"chat_id": TG_CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=data)
        print("✅ Message sent!" if r.status_code == 200 else r.text)
    except Exception as e:
        print("❌ Telegram error:", e)

def check_stock(name, url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        html = res.text
        if "Currently unavailable" not in html:
            print(f"✅ {name} is in stock!")
            send_telegram(f"✅ {name} is in stock! Buy now:\n{url}")
        else:
            print(f"❌ {name} still out of stock.")
    except Exception as e:
        print(f"❌ Error checking {name}: {e}")

if __name__ == "__main__":
    while True:
        print("🔁 Checking stock for all products...")
        for name, url in PRODUCTS.items():
            check_stock(name, url)
        print("⏳ Waiting 30 minutes...\n")
        time.sleep(1800)  # Wait 30 minutes (1800 seconds)

