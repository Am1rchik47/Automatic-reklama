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

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

date_today_str = today.strftime("%d.%m.%Y")
date_tomorrow_str = tomorrow.strftime("%d.%m.%Y")

day_today_name = DAYS_OF_WEEK[today.weekday()]
day_tomorrow_name = DAYS_OF_WEEK[tomorrow.weekday()]

post_text_vk = f"""Есть места 📞8(927)08-80-720 
🌞{date_today_str} {day_today_name}
🌞{date_tomorrow_str} {day_tomorrow_name}
🚕Исянгулово-Мраково-Уфа-Мраково-Исянгулово 
✅Выдаём билеты с QR-кодом 
📌Заберём со всех попутных городов и деревень 
📌В любое удобное для Вас время 
📌Курьерские услуги 
📌Онлайн оплата"""

post_text_tg = f"```\n{post_text_vk}\n```"

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
    url_tg = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params_tg = {"chat_id": TELEGRAM_CHAT_ID, "text": post_text_tg, "parse_mode": "MarkdownV2"}
    res_tg = requests.post(url_tg, json=params_tg).json()
    if res_tg.get("ok"):
        print("Успешно отправлено в Telegram!")
    else:
        print("Ошибка Telegram:", res_tg)

VK_TOKEN = os.environ.get("VK_TOKEN")
VK_GROUP_ID = os.environ.get("VK_GROUP_ID")

if VK_TOKEN and VK_GROUP_ID:
    url_vk = "https://api.vk.com/method/wall.post"
    params_vk = {
        "owner_id": VK_GROUP_ID,
        "from_group": 1,
        "message": post_text_vk,
        "access_token": VK_TOKEN,
        "v": "5.131",
    }
    res_vk = requests.post(url_vk, data=params_vk).json()
    if "response" in res_vk:
        print("Ура! Пост успешно опубликован в группе ВК! ID поста:", res_vk["response"]["post_id"])
    else:
        print("Ошибка ВК:", res_vk)
