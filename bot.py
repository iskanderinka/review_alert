import telegram
from config import BOT_TOKEN, CHAT_IDS
from logger import logger


def send_telegram_alert(review_data):
    """
    Отправляет уведомление о негативном отзыве в Telegram нескольким пользователям.

    Args:
        review_data (dict): Данные об отзыве (id, rating, text, link, username)
    """
    success_count = 0
    total_count = len(CHAT_IDS)

    for chat_id in CHAT_IDS:
        try:
            # Создаем экземпляр бота
            bot = telegram.Bot(token=BOT_TOKEN)

            # Формируем сообщение
            message = format_alert_message(review_data)

            # Отправляем сообщение
            bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')

            logger.info(f"Уведомление об отзыве {review_data['id']} отправлено в Telegram для chat_id: {chat_id}")
            success_count += 1

        except telegram.error.TelegramError as e:
            logger.error(f"Ошибка отправки в Telegram для chat_id {chat_id}: {e}")
        except Exception as e:
            logger.error(f"Неожиданная ошибка при отправке в Telegram для chat_id {chat_id}: {e}")

    logger.info(f"Отправлено {success_count} из {total_count} уведомлений")
    return success_count > 0  # Возвращаем True, если хотя бы одно уведомление отправлено


def format_alert_message(review_data):
    """
    Форматирует сообщение о негативном отзыве для Telegram.

    Args:
        review_data (dict): Данные об отзыве

    Returns:
        str: Отформатированное сообщение
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
