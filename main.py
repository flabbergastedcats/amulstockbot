import os
import time
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env or Render dashboard
load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_IDS = [
    os.getenv("TG_CHAT_ID"),
    os.getenv("SECOND_CHAT_ID")
]

# ✅ Product URLs
PRODUCT_URLS = {
    "Amul Protein Buttermilk (Amazon)": "https://www.amazon.in/Amul-Protein-Buttermilk-protein-8x200mL/dp/B09RV8YWWT",
    "Amul High Protein Buttermilk (
