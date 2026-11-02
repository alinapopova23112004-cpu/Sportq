import feedparser
import requests
import argparse
from datetime import datetime
import pytz

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = "СЮДА_ТОКЕН"
CHANNEL_ID = "@твой_канал"

RSS_URL = "https://www.sports.ru/rss/topnews.xml"
NEWS_COUNT = 5
# ================================================

MOSCOW_TZ = pytz.timezone("Europe/Moscow")

def get_news():
    feed = feedparser.parse(RSS_URL)
    news = []

    keywords = ["футбол", "хоккей", "рпл", "кхл", "нхл", "апел", "ла лига", 
                "серия а", "бундеслига", "лига чемпионов", "лига европы",
                "спартак", "зенит", "цска", "динамо", "локомотив", "краснодар",
                "ювентус", "реал", "барселона", "ливерпуль", "арсенал", "манчестер"]

    for entry in feed.entries:
        title = entry.title.lower()
        summary = getattr(entry, "summary", "").lower()

        if any(kw in title or kw in summary for kw in keywords):
            news.append({
                "title": entry.title,
                "link": entry.link
            })

        if len(news) >= NEWS_COUNT:
            break

    return news

def morning_message():
    news = get_news()
    
    text = "🗓 <b>РАСПИСАНИЕ ГЛАВНЫХ МАТЧЕЙ НА СЕГОДНЯ!</b> 🗓\n\n"
    text += "Собрали для вас самые важные футбольные и хоккейные события дня. День обещает быть горячим! 🔥\n\n"
    
    text += "⚽ <b>Футбол:</b>\n"
    text += "• <a href='https://www.sports.ru/football/'>Полное расписание на Sports.ru</a>\n"
    text += "• <a href='https://www.livesport.ru/football/'>LiveSport</a>\n\n"
    
    text += "🏒 <b>Хоккей:</b>\n"
    text += "• <a href='https://www.sports.ru/hockey/'>Расписание на Sports.ru</a>\n"
    text += "• <a href='https://www.khl.ru/'>Официальный сайт КХЛ</a>\n\n"
    
    text += "──────────────\n"
    text += "🔥 <b>Свежие новости утра:</b>\n\n"
    
    for i, item in enumerate(news, 1):
        text += f"<b>{i}. {item['title']}</b>\n"
        text += f"<a href='{item['link']}'>Читать полностью →</a>\n\n"
    
    text += "──────────────\n"
    text += "👇 <b>Какой матч будешь смотреть сегодня?</b> Пиши в комментариях!"
    
    return text

def day_message():
    news = get_news()
    
    text = "🔥 <b>СВЕЖИЕ СПОРТИВНЫЕ НОВОСТИ</b> 🔥\n\n"
    text += "Самое важное, что происходит прямо сейчас в мире футбола и хоккея:\n\n"
    
    for i, item in enumerate(news, 1):
        text += f"<b>{i}. {item['title']}</b>\n"
        text += f"<a href='{item['link']}'>Читать →</a>\n\n"
    
    text += "──────────────\n"
    text += "🔥 Оставайся с нами, чтобы ничего не пропустить!\n"
    text += "👇 Что думаешь по поводу этих новостей? Пиши в комментариях!"
    
    return text

def evening_message():
    news = get_news()
    
    text = "🌙 <b>ВЕЧЕРНИЕ НОВОСТИ | ИТОГИ ДНЯ</b> 🌙\n\n"
    text += "Подводим итоги насыщенного спортивного дня:\n\n"
    
    for i, item in enumerate(news, 1):
        text += f"<b>{i}. {item['title']}</b>\n"
        text += f"<a href='{item['link']}'>Читать →</a>\n\n"
    
    text += "──────────────\n"
    text += "🔥 Спасибо, что были с нами сегодня!\n"
    text += "👇 Какой момент дня запомнился больше всего? Пиши в комментариях!"
    
    return text

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    r = requests.post(url, data=payload, timeout=15)
    if r.status_code == 200:
        print("✅ Сообщение отправлено")
    else:
        print("❌ Ошибка:", r.text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["morning", "day", "evening"], required=True)
    args = parser.parse_args()

    now = datetime.now(MOSCOW_TZ)
    print(f"Время: {now.strftime('%d.%m.%Y %H:%M')} | Режим: {args.mode}")

    if args.mode == "morning":
        text = morning_message()
    elif args.mode == "day":
        text = day_message()
    else:
        text = evening_message()

    send_message(text)

if __name__ == "__main__":
    main()
    
