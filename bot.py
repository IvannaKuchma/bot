import asyncio
import os
import requests
from telegram import Bot
print("BOT STARTED OK", flush=True)


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])
INTERVAL = int(os.environ.get("INTERVAL", 240))  # 240 сек = 4 хв
STATUS_INTERVAL = int(os.environ.get("STATUS_INTERVAL", 3 * 60 * 60))  # 3 години


URL = "https://toronto.pasport.org.ua/solutions/e-queue"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Accept-Language": "uk-UA,uk;q=0.9,en;q=0.8",
}

bot = Bot(token=BOT_TOKEN)
last_state = False  # пам'ятаємо попередній стан


def has_slots():
    """Повертає True якщо, ймовірно, є слоти. На 403/помилках — None."""
    try:
        r = requests.get(URL, headers=HEADERS, timeout=20)

        # якщо сайт блокує (403) або інша помилка — просто пропускаємо цикл
        if r.status_code != 200:
            return None

        text = r.text.lower()

        no_slots_phrases = [
            "вільних місць немає",
            "немає доступних",
            "no available",
        ]

        return not any(p in text for p in no_slots_phrases)

    except Exception:
        return None


async def main():
    global last_state

    print("ENTERING LOOP", flush=True)

    await bot.send_message(
        chat_id=CHAT_ID,
        text="🤖 Бот запущений 24/7. Напишу, коли зʼявляться слоти + буду давати статус кожні кілька годин."
    )

    last_status_ts = 0  # коли востаннє шлали статус

    while True:
        current = has_slots()
        now = asyncio.get_event_loop().time()

        # 1) Термінове повідомлення: слоти з'явилися
        if current is True and last_state is False:
            await bot.send_message(
                chat_id=CHAT_ID,
                text="🔥 ЗʼЯВИЛИСЯ СЛОТИ! Перевір швидко:\n" + URL
            )
            last_state = True

        elif current is False:
            last_state = False

        # 2) Регулярний статус раз на STATUS_INTERVAL
        if now - last_status_ts >= STATUS_INTERVAL:
            if current is True:
                msg = "✅ Статус: ймовірно Є слоти (або сторінка не містить фраз 'немає місць')."
            elif current is False:
                msg = "❌ Статус: слотів немає."
            else:
                msg = "⚠️ Статус: не вдалося перевірити (можливий 403/капча/помилка)."

            await bot.send_message(chat_id=CHAT_ID, text=msg + "\n" + URL)
            last_status_ts = now

        await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())

