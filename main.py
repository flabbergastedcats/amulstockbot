import os
import time
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

# Product URLs
PRODUCT_URLS = {
    "Amul Protein Buttermilk": "https://www.amazon.in/Amul-Protein-Buttermilk-protein-8x200mL/dp/B09RV8YWWT"
}

def check_stock():
    for product_name, url in PRODUCT_URLS.items():
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            status = soup.select_one("#availability span")
            if status and "In Stock" in status.get_text():
                message = f"✅ {product_name} is back in stock!\n{url}"
            else:
                message = f"❌ {product_name} still out of stock."
            print(message)
            send_telegram(message)
        except Exception as e:
            print(f"Error: {e}")
            send_telegram(f"⚠️ Error checking {product_name}: {e}")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Telegram error: {response.text}")
    except Exception as e:
        print(f"Telegram send failed: {e}")

def bot_loop():
    while True:
        check_stock()
        time.sleep(300)  # 5 mins

# Flask app to satisfy Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

if __name__ == "__main__":
    # Start the stock checker in the background
    threading.Thread(target=bot_loop, daemon=True).start()

    # Start Flask on Render-assigned port
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
