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

# Твой родной текст
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

post_text_tg = f"```\n{post_text_vk}\n
```"

VK_TOKEN = os.environ.get("VK_TOKEN")
VK_GROUP_ID = os.environ.get("VK_GROUP_ID")

# Флаг, нужно ли отправлять пост (по умолчанию - да)
need_to_post = True

if VK_TOKEN and VK_GROUP_ID:
    # --- ПРОВЕРКА: ЧТО СЕЙЧАС НАВЕРХУ СТЕНЫ ---
    url_get = "https://api.vk.com/method/wall.get"
    params_get = {
        "owner_id": VK_GROUP_ID,
        "count": 2, # Берём парочку, на случай если первый пост закреплен
        "access_token": VK_TOKEN,
        "v": "5.131"
    }
    try:
        res_get = requests.post(url_get, data=params_get).json()
        if "response" in res_get and res_get["response"]["items"]:
            # Берем самую верхнюю запись на стене
            latest_post = res_get["response"]["items"][0]
            latest_text = latest_post.get("message", "")
            
            # Проверяем, есть ли в этом посте твой номер телефона и фраза "Есть места"
            if "Есть места" in latest_text and "8(927)08-80-720" in latest_text:
                print("Наверху стены уже висит наше объявление! Пропускаем этот запуск.")
                need_to_post = False
    except Exception as e:
        print("Не удалось проверить стену, публикуем на всякий случай. Ошибка:", e)

# --- ЕСЛИ НАВЕРХУ НЕТ НАШЕГО ПОСТА, ТО ЗАПУСКАЕМ РЕКЛАМУ ---
if need_to_post:
    # 1. ОТПРАВКА В TELEGRAM
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

    # 2. ОТПРАВКА В ВКОНТАКТЕ
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
            print("Ура! Пост успешно опубликован в группе ВК!")
        else:
            print("Ошибка публикации в ВК:", res_vk)
else:
    print("Робот ничего не отправил, так как реклама уже на месте. Ждем следующие 3 часа.")
