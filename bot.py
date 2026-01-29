import asyncio
import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])
INTERVAL = int(os.environ.get("INTERVAL", 120))

URL = "https://toronto.pasport.org.ua/solutions/e-queue"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "uk-UA,uk;q=0.9,en;q=0.8",
}

bot = Bot(token=BOT_TOKEN)

def check_slots():
    r = requests.get(URL, headers=HEADERS, timeout=20)
    if r.status_code != 200:
        return f"❌ Помилка сайту: {r.status_code}"

    text = r.text.lower()

    no_slots = [
        "вільних місць немає",
        "немає доступних",
        "no available"
    ]

    if any(x in text for x in no_slots):
        return "⛔ Слотів немає"
    else:
        return "🔥 МОЖЛИВО є слоти! Перевір сайт вручну"

async def main():
    await bot.send_message(chat_id=CHAT_ID, text="🤖 Бот запущений 24/7")

    while True:
        result = check_slots()
        await bot.send_message(chat_id=CHAT_ID, text=result)
        await asyncio.sleep(INTERVAL)

asyncio.run(main())

