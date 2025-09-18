import logging
from logging.handlers import RotatingFileHandler
import os
from config import BASE_DIR

# Абсолютный путь к папке логов
LOG_DIR = os.path.join(BASE_DIR, 'logs')

def setup_logger():
    """
    Настройка системы логирования с ротацией файлов.
    """
    # Создаем папку для логов, если ее нет
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Создаем логгер
    logger = logging.getLogger('review_bot')
    logger.setLevel(logging.INFO)

    # Форматирование сообщений
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Обработчик для записи в файл с ротацией
    log_file = os.path.join(LOG_DIR, 'bot.log')
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1*1024*1024,  # 1 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Создаем глобальный экземпляр логгера
logger = setup_logger()