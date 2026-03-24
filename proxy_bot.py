import asyncio
from telegram import Bot
from telegram.request import HTTPXRequest
from config import PROXY_URL, BOT_TOKEN
from logger import logger

_bot = None

def get_bot():
    """Возвращает экземпляр Bot, настроенный на работу через прокси (если указан)."""
    global _bot
    if _bot is None:
        if PROXY_URL:
            logger.info(f"Используем прокси: {PROXY_URL}")
            request = HTTPXRequest(proxy_url=PROXY_URL)
            _bot = Bot(token=BOT_TOKEN, request=request)
        else:
            logger.info("Прокси не настроен, используем прямое подключение")
            _bot = Bot(token=BOT_TOKEN)
    return _bot