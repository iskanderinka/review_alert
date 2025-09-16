import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    """
    Настройка системы логирования с ротацией файлов.
    Создает логгер с выводом в консоль и файл с ротацией.
    """
    # Создаем папку для логов, если ее нет
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Создаем логгер
    logger = logging.getLogger('review_bot')
    logger.setLevel(logging.INFO)

    # Форматирование сообщений
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Обработчик для записи в файл с ротацией
    file_handler = RotatingFileHandler(
        'logs/bot.log',
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