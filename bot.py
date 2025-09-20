# bot.py
import asyncio
import telegram
import time
from config import BOT_TOKEN, CHAT_IDS
from logger import logger


async def send_telegram_alert(review_data):
    """
    Асинхронно отправляет уведомление о негативном отзыве в Telegram нескольким пользователям.
    С механизмом повторных попыток.
    """
    if not CHAT_IDS:
        logger.error("Нет chat_id для отправки уведомлений")
        return False

    success_count = 0
    total_count = len(CHAT_IDS)

    for i, chat_id in enumerate(CHAT_IDS):
        max_retries = 3
        retry_delay = 2  # секунды

        for attempt in range(max_retries):
            try:
                # Добавляем задержку между отправками (1 секунда)
                if i > 0:
                    await asyncio.sleep(1)

                # Создаем экземпляр бота для каждой попытки
                bot = telegram.Bot(token=BOT_TOKEN)

                # Формируем сообщение
                message = format_alert_message(review_data)

                # Отправляем сообщение
                await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')

                logger.info(f"Уведомление об отзыве {review_data['id']} отправлено в Telegram для chat_id: {chat_id}")
                success_count += 1
                break  # Успешно отправили, выходим из цикла повторных попыток

            except telegram.error.Forbidden as e:
                logger.error(f"Ошибка авторизации для chat_id {chat_id}: {e}. Возможно, бот заблокирован.")
                break  # Не будем повторять для этой ошибки
            except (telegram.error.TimedOut, telegram.error.NetworkError, telegram.error.RetryAfter) as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Попытка {attempt + 1}/{max_retries} не удалась для chat_id {chat_id}. Повтор через {retry_delay} сек.: {e}")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Увеличиваем задержку для следующей попытки
                else:
                    logger.error(f"Все {max_retries} попыток не удались для chat_id {chat_id}: {e}")
            except telegram.error.BadRequest as e:
                logger.error(f"Неверный запрос для chat_id {chat_id}: {e}. Проверьте правильность chat_id.")
                break  # Не будем повторять для этой ошибки
            except Exception as e:
                logger.error(f"Неожиданная ошибка для chat_id {chat_id}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error(f"Все {max_retries} попыток не удались для chat_id {chat_id}: {e}")

    logger.info(f"Отправлено {success_count} из {total_count} уведомлений")
    return success_count > 0

# format_alert_message функция остается без изменений