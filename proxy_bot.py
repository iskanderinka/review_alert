import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector
from telegram import Bot
from config import PROXY_URL, BOT_TOKEN
from logger import logger

_bot = None

def get_bot():
    """Возвращает экземпляр Bot, настроенный на работу через прокси (если указан)."""
    global _bot
    if _bot is None:
        if PROXY_URL:
            logger.info(f"Используем прокси: {PROXY_URL}")
            connector = ProxyConnector.from_url(PROXY_URL)
            session = aiohttp.ClientSession(connector=connector)
            _bot = Bot(token=BOT_TOKEN, session=session)
        else:
            _bot = Bot(token=BOT_TOKEN)
    return _bot