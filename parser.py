import requests
import re
from bs4 import BeautifulSoup
from config import SITE_URL, HEADERS, SELECTORS
from logger import logger
from storage import generate_review_hash


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

        reviews = []

        for i, container in enumerate(review_containers):
            try:
                # Извлекаем рейтинг
                rating = extract_rating(container)

                # Извлекаем текст отзыва
                text = extract_review_text(container)

                # Извлекаем имя пользователя
                username = extract_username(container)

                # Извлекаем ссылку на поход
                link = extract_trip_link(container)

                # Пытаемся извлечь стабильный ID отзыва
                review_id = extract_review_id(container, i)
                
                # Если не удалось извлечь стабильный ID, создаем хэш на основе содержимого
                if review_id.startswith('temp_id_'):
                    review_data_for_hash = {
                        'username': username,
                        'text': text,
                        'rating': rating
                    }
                    review_id = generate_review_hash(review_data_for_hash)

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
    Пытается найти стабильный ID несколькими способами.
    """
    try:
        # Способ 1: Ищем ID в data-fancybox атрибуте
        photo_link = container.select_one(SELECTORS['photo_link'])
        if photo_link and photo_link.get('data-fancybox'):
            data_fancybox = photo_link['data-fancybox']
            match = re.search(r'review-(\d+)', data_fancybox)
            if match:
                return match.group(1)

        # Способ 2: Ищем ID в атрибутах самого контейнера
        if container.get('id'):
            return container['id']

        # Способ 3: Ищем ID в данных о отзыве
        data_review = container.get('data-review')
        if data_review:
            match = re.search(r'id["\']:\s*["\']?(\d+)', data_review)
            if match:
                return match.group(1)

        # Если ничего не нашли, используем временный ID (будет заменен на хэш позже)
        return f"temp_id_{index}"
    except Exception as e:
        logger.error(f"Ошибка при извлечении ID отзыва: {e}")
        return f"temp_id_{index}"

# Остальные функции extract_rating, extract_review_text, extract_trip_link, extract_username остаются без изменений