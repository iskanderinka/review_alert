import json
import os
from logger import logger
from config import BASE_DIR

# Абсолютный путь к файлу хранилища
STORAGE_FILE = os.path.join(BASE_DIR, 'processed_reviews.json')


def load_processed_reviews():
    """
    Загружает множество ID обработанных отзывов из JSON-файла.
    """
    logger.info(f"Пытаемся загрузить обработанные отзывы из файла: {STORAGE_FILE}")

    if not os.path.exists(STORAGE_FILE):
        logger.info(f"Файл {STORAGE_FILE} не существует, возвращаем пустой набор")
        return set()

    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"Загружено {len(data)} обработанных отзывов из файла {STORAGE_FILE}")
            return set(data)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Ошибка загрузки файла хранилища: {e}")
        return set()


def save_processed_reviews(review_ids):
    """
    Сохраняет множество ID обработанных отзывов в JSON-файл.
    """
    try:
        data = list(review_ids)
        with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Сохранено {len(data)} ID отзывов в файл {STORAGE_FILE}")
    except Exception as e:
        logger.error(f"Ошибка сохранения ID отзывов: {e}")


def add_processed_review(review_id):
    """
    Добавляет один ID отзыва в хранилище.
    """
    processed = load_processed_reviews()
    processed.add(review_id)
    save_processed_reviews(processed)