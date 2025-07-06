import asyncio
import requests
from telegram import Bot
from telegram.constants import ParseMode

    # 🔐 Токен бота
TOKEN = '7928801571:AAElQ_J6qieo6pvggLwinsZd4Q6YiFBpXOc'

    # 📢 Канал
CHANNEL_ID = '@ichnya'

    # 🌍 ID області (Чернігівська = 3)
REGION_ID = 24

bot = Bot(token=TOKEN)
previous_alert = None  # Стартове значення

async def check_alerts():
        global previous_alert
        url = "https://alerts.com.ua/api/states"

        while True:
            try:
                response = requests.get(url)
                print(f"[LOG] Статус запиту: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    states = data.get("states", [])

                    region = next((r for r in states if r.get("id") == REGION_ID), None)

                    if region:
                        current_alert = region.get("alert", False)
                        print(f"[DEBUG] Поточний: {current_alert}, Попередній: {previous_alert}")

                        if previous_alert is None:
                            # 🟡 Перше повідомлення після запуску
                            previous_alert = current_alert
                            msg = "🚨 Тривога активна на момент запуску." if current_alert else "✅ Відбій тривоги на момент запуску."
                            await bot.send_message(chat_id=CHANNEL_ID, text=f"▶️ Бот запущено\n{msg}")
                        elif current_alert != previous_alert:
                            # 🔄 Статус змінився
                            previous_alert = current_alert
                            if current_alert:
                                await bot.send_message(chat_id=CHANNEL_ID, text="🚨 Повітряна тривога в Чернігівській області!")
                            else:
                                await bot.send_message(chat_id=CHANNEL_ID, text="✅ Відбій повітряної тривоги.")
                        else:
                            print("[INFO] Стан не змінився.")
                    else:
                        print(f"[WARN] Область з ID {REGION_ID} не знайдена в API")
                else:
                    print(f"[ERROR] Помилка HTTP: {response.status_code}")

            except Exception as e:
                print(f"[EXCEPTION] Виняток при запиті: {e}")

            await asyncio.sleep(30)  # 🔁 Перевіряємо кожні 30 секунд

async def main():
        await check_alerts()

if __name__ == '__main__':
        asyncio.run(main())
