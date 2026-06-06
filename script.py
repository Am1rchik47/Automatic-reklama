import datetime
import os
import requests

# Список дней недели на русском
DAYS_OF_WEEK = [
    "понедельник",
    "вторник",
    "среда",
    "четверг",
    "пятница",
    "суббота",
    "воскресенье",
]

# Вычисляем даты (сегодня и завтра)
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

date_today_str = today.strftime("%d.%m.%Y")
date_tomorrow_str = tomorrow.strftime("%d.%m.%Y")

day_today_name = DAYS_OF_WEEK[today.weekday()]
day_tomorrow_name = DAYS_OF_WEEK[tomorrow.weekday()]

# Собираем текст поста и заворачиваем его в тройные обратные кавычки ```
# Это сделает весь текст внутри копируемым в 1 клик
post_text = f"""```
Есть места 📞8(927)08-80-720 
🌞{date_today_str} {day_today_name}
🌞{date_tomorrow_str} {day_tomorrow_name}
🚕Исянгулово-Мраково-Уфа-Мраково-Исянгулово 
✅Выдаём билеты с QR-кодом 
📌Заберём со всех попутных городов и деревень 
📌В любое удобное для Вас время 
📌Курьерские услуги 
📌Онлайн оплата
```"""

# Достаем секретные ключи из настроек GitHub
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Отправляем сообщение в Telegram (добавили parse_mode)
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
params = {
    "chat_id": TELEGRAM_CHAT_ID, 
    "text": post_text,
    "parse_mode": "MarkdownV2"  # Включаем поддержку красивого форматирования
}

response = requests.post(url, json=params).json()

if response.get("ok"):
    print("Ура! Текст успешно отправлен в Telegram!")
else:
    print("Ошибка отправки:", response)
