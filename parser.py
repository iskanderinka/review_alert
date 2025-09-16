import requests
import re
from bs4 import BeautifulSoup
from config import SITE_URL, HEADERS, SELECTORS
from logger import logger


def get_reviews():
    """
    Получает и парсит отзывы с сайта turclub-pik.ru.
    """
    try:
        logger.info(f"Начинаем парсинг страницы: {SITE_URL}")

        # Отправляем HTTP-запрос к сайту
        response = requests.get(SITE_URL, headers=HEADERS, timeout=30)
        response.raise_for_status()

        # Парсим HTML-контент
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем все контейнеры с отзывами
        review_containers = soup.select(SELECTORS['review_container'])
        logger.info(f"Найдено {len(review_containers)} контейнеров отзывов")

        # Ограничиваемся первыми 20 отзывами
        review_containers = review_containers[:20]
        reviews = []

        for i, container in enumerate(review_containers):
            try:
                # Извлекаем ID отзыва
                review_id = extract_review_id(container, i)

                # Извлекаем рейтинг
                rating = extract_rating(container)

                # Извлекаем текст отзыва
                text = extract_review_text(container)

                # Извлекаем ссылку на поход
                link = extract_trip_link(container)

                # Извлекаем имя пользователя
                username = extract_username(container)

                review_data = {
                    'id': review_id,
                    'rating': rating,
                    'text': text,
                    'link': link,
                    'username': username
                }

                reviews.append(review_data)

            except Exception as e:
                logger.error(f"Ошибка при обработке отзыва: {e}")
                continue

        logger.info(f"Успешно обработано {len(reviews)} отзывов")
        return reviews

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к сайту: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка в парсере: {e}")
        return []


def extract_review_id(container, index):
    """
    Извлекает уникальный идентификатор отзыва.
    """
    try:
        # Ищем первую ссылку на фото
        photo_link = container.select_one(SELECTORS['photo_link'])
        if photo_link and photo_link.get('data-fancybox'):
            # Извлекаем ID из data-fancybox="review-5867"
            data_fancybox = photo_link['data-fancybox']
            match = re.search(r'review-(\d+)', data_fancybox)
            if match:
                return match.group(1)

        # Если не нашли, используем индекс как временный ID
        return f"temp_id_{index}"
    except Exception as e:
        logger.error(f"Ошибка при извлечении ID отзыва: {e}")
        return f"temp_id_{index}"


def extract_rating(container):
    """
    Извлекает рейтинг отзыва, подсчитывая активные звезды.
    """
    try:
        rating_container = container.select_one(SELECTORS['rating_container'])
        if rating_container:
            active_stars = rating_container.select(SELECTORS['active_star'])
            return len(active_stars)
        return 0
    except Exception as e:
        logger.error(f"Ошибка при извлечении рейтинга: {e}")
        return 0


def extract_review_text(container):
    """
    Извлекает текст отзыва.
    """
    try:
        text_element = container.select_one(SELECTORS['review_text'])
        if text_element:
            return text_element.get_text(strip=True)
        return "Текст отзыва отсутствует"
    except Exception as e:
        logger.error(f"Ошибка при извлечении текста отзыва: {e}")
        return "Текст отзыва отсутствует"


def extract_trip_link(container):
    """
    Извлекает ссылку на поход.
    """
    try:
        link_element = container.select_one(SELECTORS['trip_link'])
        if link_element and link_element.get('href'):
            link = link_element['href']
            if not link.startswith('http'):
                return f"https://turclub-pik.ru{link}"
            return link
        return SITE_URL
    except Exception as e:
        logger.error(f"Ошибка при извлечении ссылки на поход: {e}")
        return SITE_URL


def extract_username(container):
    """
    Извлекает имя пользователя, оставившего отзыв.
    """
    try:
        username_element = container.select_one(SELECTORS['username'])
        if username_element:
            # Убираем лишние пробелы и переносы строк
            username_text = username_element.get_text(strip=True)
            # Убираем текст после имени (если есть)
            username = username_text.split('\n')[0].strip()
            return username
        return "Анонимный пользователь"
    except Exception as e:
        logger.error(f"Ошибка при извлечении имени пользователя: {e}")
        return "Анонимный пользователь"