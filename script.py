import datetime
import os
import requests

DAYS_OF_WEEK = [
    "понедельник",
    "вторник",
    "среда",
    "четверг",
    "пятница",
    "суббота",
    "воскресенье",
]

# Вычисляем время по Уфе
utc_now = datetime.datetime.utcnow()
ufa_now = utc_now + datetime.timedelta(hours=5)

today = ufa_now.date()
tomorrow = today + datetime.timedelta(days=1)

date_today_str = today.strftime("%d.%m.%Y")
date_tomorrow_str = tomorrow.strftime("%d.%m.%Y")

day_today_name = DAYS_OF_WEEK[today.weekday()]
day_tomorrow_name = DAYS_OF_WEEK[tomorrow.weekday()]

# Твой родной лаконичный текст
post_text_vk = f"""Есть места 📞8(927)08-80-720 
🌞{date_today_str} {day_today_name}
🌞{date_tomorrow_str} {day_tomorrow_name}
🚕Исянгулово-Мраково-Уфа-Мраково-Исянгулово 
✅Выдаём билеты с QR-кодом 
📌Заберём со всех попутных городов и деревень 
📌В любое удобное для Вас время 
📌Курьерские услуги 
📌Онлайн оплата

🔥Сообщество VK:
https://vk.com/uldashsoo"""

# --- ОТПРАВКА В TELEGRAM ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
    url_tg = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params_tg = {"chat_id": TELEGRAM_CHAT_ID, "text": post_text_vk}
    try:
        requests.post(url_tg, json=params_tg)
        print("Отправлено в Telegram")
    except:
        pass

# --- ОТПРАВКА В ВКОНТАКТЕ ---
VK_TOKEN = os.environ.get("VK_TOKEN")
VK_GROUP_ID = os.environ.get("VK_GROUP_ID")

if VK_TOKEN and VK_GROUP_ID:
    url_vk_post = "https://api.vk.com/method/wall.post"
    params_vk_post = {
        "owner_id": VK_GROUP_ID,
        "from_group": 1,
        "message": post_text_vk,
        "access_token": VK_TOKEN,
        "v": "5.131",
    }
    try:
        res_vk = requests.post(url_vk_post, data=params_vk_post).json()
        if "response" in res_vk:
            print("Успешно опубликовано в ВК!")
        else:
            print("Ошибка ВК:", res_vk)
    except Exception as e:
        print("Ошибка сети:", e)
