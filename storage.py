import json
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FILE = os.path.join(BASE_DIR, 'processed_reviews.json')
from logger import logger

# Имя файла для хранения обработанных отзывов
STORAGE_FILE = 'processed_reviews.json'

def load_processed_reviews():
    """
    Загружает множество ID обработанных отзывов из JSON-файла.
    """
    if not os.path.exists(STORAGE_FILE):
        return set()

    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
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
    except Exception as e:
        logger.error(f"Ошибка сохранения ID отзывов: {e}")

def add_processed_review(review_id):
    """
    Добавляет один ID отзыва в хранилище.
    """
    processed = load_processed_reviews()
    processed.add(review_id)
    save_processed_reviews(processed)