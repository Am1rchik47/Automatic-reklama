import datetime
import os
import requests
import time

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
📌Онлайн оплата

🔥Сообщество VK:
https://vk.com/uldashsoo"""

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
    url_vk_post = "https://api.vk.com/method/wall.post"
    params_vk_post = {
        "owner_id": VK_GROUP_ID,
        "from_group": 1,
        "message": post_text_vk,
        "access_token": VK_TOKEN,
        "v": "5.131",
    }
    res_vk = requests.post(url_vk_post, data=params_vk_post).json()
    
    if "response" in res_vk:
        post_id = res_vk["response"]["post_id"]
        print(f"Пост успешно опубликован в ВК! ID: {post_id}")
        
        time.sleep(3)
        
        url_vk_pin = "https://api.vk.com/method/wall.pin"
        params_vk_pin = {
            "owner_id": VK_GROUP_ID,
            "post_id": post_id,
            "access_token": VK_TOKEN,
            "v": "5.131",
        }
        res_pin = requests.post(url_vk_pin, data=params_vk_pin).json()
        if "response" in res_pin:
            print("Пост успешно закреплен на стене ВК!")
        else:
            print("Не удалось закрепить пост в ВК. Ответ сервера:", res_pin)
    else:
        print("Ошибка публикации в ВК:", res_vk)
