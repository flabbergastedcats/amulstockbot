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

# List of product URLs
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
            print(f"Error checking stock: {e}")
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
            print(f"❌ Failed to send message: {response.text}")
    except Exception as e:
        print(f"❌ Telegram send error: {e}")

# Background loop
def run_bot():
    while True:
        check_stock()
        time.sleep(300)  # check every 5 mins

# Dummy Flask server to satisfy Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # use Render's assigned port
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=port)
