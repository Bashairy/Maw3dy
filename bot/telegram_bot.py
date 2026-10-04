import asyncio
import os

from dotenv import load_dotenv
from telegram import Bot


# تحميل بيانات .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


async def send_booking_notification(name, phone, date, time):
    message = f"""
🔔 حجز جديد في Maw3dy

👤 الاسم: {name}
📞 الهاتف: {phone}
📅 التاريخ: {date}
⏰ الوقت: {time}

✅ الحالة: مؤكد
"""

    bot = Bot(token=BOT_TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )


def notify_booking(name, phone, date, time):
    asyncio.run(
        send_booking_notification(
            name,
            phone,
            date,
            time
        )
    )