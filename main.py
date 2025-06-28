import os
import time
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask
from dotenv import load_dotenv

# Load .env (for local) or Render ENV (in production)
load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_IDS = [
    os.getenv("TG_CHAT_ID"),
    os.getenv("SECOND_CHAT_ID")
]

# ✅ Product list
PRODUCT_URLS = {
    "Amul Protein Buttermilk (Amazon)": "https://www.amazon.in/Amul-Protein-Buttermilk-protein-8x200mL/dp/B09RV8YWWT",
    "Amul High Protein Buttermilk (Amul Store)": "https://shop.amul.com/en/product/amul-high-protein-buttermilk-200-ml-or-pack-of-30",
    "Amul Chocolate Whey Protein (Amul Store)": "https://shop.amul.com/en/product/amul-chocolate-whey-protein-34-g-or-pack-of-30-sachets"
}

# ✅ Stock checking function
def check_stock():
    for product_name, url in PRODUCT_URLS.items():
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Logic for each site
            if "amazon.in" in url:
                status = soup.select_one("#availability span")
                in_stock = status and "In Stock" in status.get_text()
            elif "shop.amul.com" in url:
                button = soup.select_one(".product-actions button.add-to-cart")
                in_stock = button and "Add to Cart" in button.get_text()
            else:
                in_stock = False

            message = (
                f"✅ {product_name} is back in stock!\n{url}"
                if in_stock else
                f"❌ {product_name} still out of stock."
            )

            print(message)
            send_telegram(message)

        except Exception as e:
            error_msg = f"⚠️ Error checking {product_name}: {e}"
            print(error_msg)
            send_telegram(error_msg)

# ✅ Telegram bot sender
def send_telegram(message):
    for chat_id in TG_CHAT_IDS:
        if not chat_id:
            continue
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        try:
            response = requests.post(url, data={"chat_id": chat_id, "text": message})
            if response.status_code != 200:
                print(f"Telegram error for {chat_id}: {response.text}")
        except Exception as e:
            print(f"Telegram send failed for {chat_id}: {e}")

# 🔁 Background loop (every 12 hours)
def bot_loop():
    while True:
        check_stock()
        time.sleep(1800)  # 12 hours = 43200 seconds

# 🌐 Flask app to keep Render alive
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Stock bot is running!"

# ✅ Run Flask first, then background thread
if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
