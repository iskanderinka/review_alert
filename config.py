from dotenv import load_dotenv
import os

# Определяем базовую директорию проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, '.env'))

BOT_TOKEN = os.getenv('BOT_TOKEN')
# Получаем список chat_id, разделенных запятыми, и преобразуем в список чисел
CHAT_IDS = [int(chat_id.strip()) for chat_id in os.getenv('CHAT_IDS', '').split(',') if chat_id.strip()]
SITE_URL = "https://turclub-pik.ru/comments/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

SELECTORS = {
    'review_container': 'article.review.media',
    'rating_container': 'div.app-star-rating',
    'active_star': 'div.star.is-active',
    'review_text': 'p.comment',
    'username': 'strong.username',
    'trip_link': 'strong.username span a[href*="/pohod/"]',
    'photo_link': 'a.photo'
}