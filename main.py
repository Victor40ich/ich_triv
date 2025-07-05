import asyncio
import requests
from telegram import Bot
from telegram.constants import ParseMode

    # Токен твого Telegram-бота
TOKEN = '7928801571:AAElQ_J6qieo6pvggLwinsZd4Q6YiFBpXOc'

    # ID або username каналу
CHANNEL_ID = '@ichnya'

    # ID області (Чернігівська)
REGION_ID = 3

bot = Bot(token=TOKEN)

    # Зберігаємо попередній стан
previous_alert = None

async def check_alerts():
        global previous_alert
        url = "https://alerts.com.ua/api/states"

        while True:
            try:
                response = requests.get(url)
                print(f"Status code: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    states = data.get("states", [])

                    region = next((r for r in states if r.get("id") == REGION_ID), None)

                    if region:
                        current_alert = region.get("alert", False)

                        # Повідомляти тільки якщо стан змінився
                        if previous_alert is None:
                            previous_alert = current_alert  # перший запуск — не надсилаємо
                        elif current_alert != previous_alert:
                            previous_alert = current_alert
                            message = "🚨 Повітряна тривога!" if current_alert else "✅ Відбій тривоги"
                            print(f"Sending alert: {message}")
                            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=ParseMode.HTML)
                    else:
                        print(f"⚠️ Region with ID {REGION_ID} not found")
                else:
                    print(f"❌ Помилка при запиті: Status {response.status_code}")
            except Exception as e:
                print(f"❌ Помилка при запиті: {e}")

            await asyncio.sleep(60)  # перевіряємо кожні 60 секунд

async def main():
        await check_alerts()

if __name__ == '__main__':
        asyncio.run(main())