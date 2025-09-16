import json
import os
from logger import logger

# Имя файла для хранения обработанных отзывов
STORAGE_FILE = 'processed_reviews.json'


def load_processed_reviews():
    """
    Загружает множество ID обработанных отзывов из JSON-файла.
    Возвращает set() если файл не существует или поврежден.
    """
    if not os.path.exists(STORAGE_FILE):
        return set()

    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Преобразуем список в множество для быстрого поиска
            return set(data)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Ошибка загрузки файла хранилища: {e}")
        return set()


def save_processed_reviews(review_ids):
    """
    Сохраняет множество ID обработанных отзывов в JSON-файл.

    Args:
        review_ids (set): Множество ID отзывов для сохранения
    """
    try:
        # Преобразуем множество в список для сериализации в JSON
        data = list(review_ids)
        with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Сохранено {len(review_ids)} ID отзывов в хранилище")
    except Exception as e:
        logger.error(f"Ошибка сохранения ID отзывов: {e}")


def add_processed_review(review_id):
    """
    Добавляет один ID отзыва в хранилище и сохраняет его.

    Args:
        review_id (str): ID отзыва для добавления
    """
    processed = load_processed_reviews()
    processed.add(review_id)
    save_processed_reviews(processed)
    logger.debug(f"Добавлен отзыв {review_id} в обработанные")