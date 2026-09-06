import datetime
import os
import requests

DAYS_OF_WEEK = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

utc_now = datetime.datetime.now(datetime.timezone.utc)
ufa_now = utc_now + datetime.timedelta(hours=5)

today = ufa_now.date()
tomorrow = today + datetime.timedelta(days=1)

date_today_str = today.strftime("%d.%m.%Y")
date_tomorrow_str = tomorrow.strftime("%d.%m.%Y")

day_today_name = DAYS_OF_WEEK[today.weekday()]
day_tomorrow_name = DAYS_OF_WEEK[tomorrow.weekday()]

post_text_vk = f"""Есть места 📞8(927)08-80-720 
🌞{date_today_str} {day_today_name}
🌞{date_tomorrow_str} {day_tomorrow_name}
🚕Набираем водителей!!!
Исянгулово-Мраково-Уфа-Мраково-Исянгулово 
✅Выдаём билеты с QR-кодом 
📌Заберём со всех попутных городов и деревень 
📌В любое удобное для Вас время 
📌Курьерские услуги 
📌Онлайн оплата
🔥Сообщества VK:
https://vk.com/uldashsoo
https://vk.com/taxi_mrk_ufa"""

# --- TELEGRAM ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
    url_tg = f"https://api.telegram.org/bot{TELEGRAM_TOKEN.strip()}/sendMessage"
    params_tg = {"chat_id": TELEGRAM_CHAT_ID.strip(), "text": post_text_vk}
    try:
        res = requests.post(url_tg, json=params_tg)
        print("Telegram API Response:", res.json())
    except Exception as e:
        print("Критическая ошибка сети в TG:", e)
else:
    print("Пропущено: Переменные Telegram не настроены.")

# --- VK GROUP 1 ---
VK_TOKEN = os.environ.get("VK_TOKEN")
VK_GROUP_ID = os.environ.get("VK_GROUP_ID")

if VK_TOKEN and VK_GROUP_ID:
    owner_id = VK_GROUP_ID.strip()
    if not owner_id.startswith("-"):
        owner_id = f"-{owner_id}"

    params_vk_post = {
        "owner_id": owner_id,
        "from_group": 1,
        "message": post_text_vk,
        "access_token": VK_TOKEN.strip(),
        "v": "5.131",
    }
    try:
        res_vk = requests.post("https://api.vk.com/method/wall.post",data=params_vk_post, header=HEADERS, timeout=10).json()
        if "response" in res_vk:
            print("Успешно опубликовано в ПЕРВОЙ группе ВК!")
        else:
            print("Ошибка в первой группе ВК:", res_vk)
    except Exception as e:
        print("Ошибка сети (Первая группа):", e)
else:
    print("Пропущено: Переменные первой группы ВК не настроены.")

# --- VK GROUP 2 ---
VK_TOKEN_2 = os.environ.get("VK_TOKEN_2")
VK_GROUP_ID_2 = os.environ.get("VK_GROUP_ID_2")

if VK_TOKEN_2 and VK_GROUP_ID_2:
    owner_id_2 = VK_GROUP_ID_2.strip()
    if not owner_id_2.startswith("-"):
        owner_id_2 = f"-{owner_id_2}"

    params_vk_post_2 = {
        "owner_id": owner_id_2,
        "from_group": 1,
        "message": post_text_vk,
        "access_token": VK_TOKEN_2.strip(),
        "v": "5.131",
    }
    try:
        res_vk_2 = requests.post("https://api.vk.com/method/wall.post", data=params_vk_post_2, header=HEADERS, timeout=10).json()
        if "response" in res_vk_2:
            print("Успешно опубликовано во ВТОРОЙ группе ВК!")
        else:
            print("Ошибка во второй группе ВК:", res_vk_2)
    except Exception as e:
        print("Ошибка сети (Вторая группа):", e)
else:
    print("Пропущено: Переменные второй группы ВК не настроены.")
