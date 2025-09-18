import asyncio
import telegram
import time
from config import BOT_TOKEN, CHAT_IDS
from logger import logger


async def send_telegram_alert(review_data):
    """
    Асинхронно отправляет уведомление о негативном отзыве в Telegram нескольким пользователям.
    """
    if not CHAT_IDS:
        logger.error("Нет chat_id для отправки уведомлений")
        return False

    success_count = 0
    total_count = len(CHAT_IDS)

    # Создаем экземпляр бота один раз
    bot = telegram.Bot(token=BOT_TOKEN)

    for i, chat_id in enumerate(CHAT_IDS):
        try:
            # Добавляем задержку между отправками (1 секунда)
            if i > 0:
                await asyncio.sleep(1)

            # Формируем сообщение
            message = format_alert_message(review_data)

            # Отправляем сообщение
            await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')

            logger.info(f"Уведомление об отзыве {review_data['id']} отправлено в Telegram для chat_id: {chat_id}")
            success_count += 1

        except telegram.error.Forbidden as e:
            logger.error(f"Ошибка авторизации для chat_id {chat_id}: {e}. Возможно, бот заблокирован.")
        except telegram.error.BadRequest as e:
            logger.error(f"Неверный запрос для chat_id {chat_id}: {e}. Проверьте правильность chat_id.")
        except telegram.error.TimedOut as e:
            logger.error(f"Таймаут подключения для chat_id {chat_id}: {e}")
        except telegram.error.NetworkError as e:
            logger.error(f"Сетевая ошибка для chat_id {chat_id}: {e}")
        except telegram.error.TelegramError as e:
            logger.error(f"Ошибка Telegram API для chat_id {chat_id}: {e}")
        except Exception as e:
            logger.error(f"Неожиданная ошибка для chat_id {chat_id}: {e}")

    logger.info(f"Отправлено {success_count} из {total_count} уведомлений")
    return success_count > 0


def format_alert_message(review_data):
    """
    Форматирует сообщение о негативном отзыве для Telegram.
    """
    rating = review_data['rating']
    username = review_data['username']
    text = review_data['text']
    link = review_data['link']

    # Создаем строку с звездочками для наглядности
    stars = "★" * rating + "☆" * (5 - rating)

    # Форматируем сообщение с использованием HTML-разметки
    message = (
        f"⚠️ <b>Негативный отзыв</b> ({rating}/5)\n\n"
        f"<b>Пользователь:</b> {username}\n"
        f"<b>Рейтинг:</b> {stars}\n\n"
        f"<b>Текст отзыва:</b>\n{text[:300]}{'...' if len(text) > 300 else ''}\n\n"
        f"<a href='{link}'>Ссылка на поход</a>"
    )

    return message