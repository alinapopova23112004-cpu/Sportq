import os
import feedparser
import requests
from google import genai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Проверенные спортивные сайты (RSS)
RSS_FEEDS = [
    "https://www.championat.com/rss/news/",
    "https://www.sports.ru/rss/main.xml",
    "https://feeds.bbci.co.uk/sport/rss.xml"
]

def get_latest_news(limit_per_feed=5):
    news_list = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:limit_per_feed]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            news_list.append(f"- {title}: {summary}")
    return "\n".join(news_list)

def generate_sport_post(raw_news):
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""
    Ты — спортивный журналист и автор Telegram-канала.
    Вот свежие новости с популярных спортивных сайтов:
    {raw_news}
    
    Задание:
    1. Выбери 4 самые главные и интересные новости.
    2. Напиши из них увлекательный, живой дайджест на русском языке.
    3. Добавь подходящие спортивные эмодзи (⚽️, 🏀, 🔥, 🏆).
    4. Разделяй новости пустыми строками для удобного чтения. Не используй символы ** или ##.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text}
    resp = requests.post(url, json=payload)
    if resp.status_code == 200:
        print("Успешно опубликовано в канал!")
    else:
        raise Exception(f"Ошибка Telegram: {resp.text}")

if __name__ == "__main__":
    news = get_latest_news()
    if news:
        post = generate_sport_post(news)
        send_to_telegram(post)
