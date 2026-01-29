import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

# Читаємо .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
INTERVAL = int(os.getenv("INTERVAL", 120))  # інтервал у секундах

bot = Bot(token=BOT_TOKEN)

async def main():
    await bot.send_message(chat_id=CHAT_ID, text="🤖 Бот стартував. Слідкую за слотами…")

    toggle = True  # для чергування повідомлень
    while True:
        message = "🔥 Є слоти!" if toggle else "❌ Слотів немає"
        print("[Перевірка]", message)
        await bot.send_message(chat_id=CHAT_ID, text=message)

        toggle = not toggle  # змінюємо стан
        await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())

