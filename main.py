import asyncio
from storage import load_processed_reviews, add_processed_review
from parser import get_reviews
from bot import send_telegram_alert
from logger import logger
import telegram
from config import BOT_TOKEN, CHAT_IDS


async def check_bot_token():
    """Проверяет валидность токена бота"""
    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        bot_info = await bot.get_me()
        logger.info(f"Бот {bot_info.username} успешно авторизован")
        return True
    except telegram.error.InvalidToken:
        logger.error("Неверный токен бота. Проверьте правильность BOT_TOKEN в .env файле.")
        return False
    except Exception as e:
        logger.error(f"Ошибка при проверке токена бота: {e}")
        return False


async def verify_chat_ids():
    """Проверяет валидность chat_id"""
    if not CHAT_IDS:
        logger.error("Не указаны chat_id в файле .env")
        return []

    bot = telegram.Bot(token=BOT_TOKEN)
    valid_chat_ids = []

    for chat_id in CHAT_IDS:
        try:
            # Пробуем получить информацию о чате
            await bot.get_chat(chat_id)
            valid_chat_ids.append(chat_id)
            logger.info(f"Chat ID {chat_id} валиден")
        except telegram.error.Unauthorized:
            logger.error(f"Chat ID {chat_id} невалиден или бот заблокирован")
        except Exception as e:
            logger.error(f"Ошибка для chat ID {chat_id}: {e}")

    return valid_chat_ids


async def main():
    """
    Основная асинхронная функция приложения.
    """
    logger.info("=" * 50)
    logger.info("Запуск проверки отзывов")
    logger.info("=" * 50)

    try:
        # Проверяем токен бота
        if not await check_bot_token():
            return

        # Проверяем chat_id
        valid_chat_ids = await verify_chat_ids()
        if not valid_chat_ids:
            logger.error("Нет валидных chat_id для отправки уведомлений")
            return

        # Загружаем ID уже обработанных отзывов
        processed_reviews = load_processed_reviews()
        logger.info(f"Загружено {len(processed_reviews)} обработанных отзывов")

        # Получаем новые отзывы с сайта (синхронная функция)
        reviews = get_reviews()

        if not reviews:
            logger.warning("Не удалось получить отзывы или список пуст")
            return

        # Фильтруем отзывы: оставляем только негативные и новые
        negative_reviews = []
        for review in reviews:
            # Пропускаем уже обработанные отзывы
            if review['id'] in processed_reviews:
                continue

            # Проверяем рейтинг (1-3 звезды)
            if 1 <= review['rating'] <= 3:
                logger.info(f"Найден негативный отзыв: ID {review['id']}, рейтинг {review['rating']}")
                negative_reviews.append(review)
            else:
                # Помечаем позитивные отзывы как обработанные, чтобы не проверять их снова
                add_processed_review(review['id'])

        # Отправляем уведомления о негативных отзывах
        sent_count = 0
        for review in negative_reviews:
            success = await send_telegram_alert(review)
            if success:
                # Помечаем отзыв как обработанный только после успешной отправки
                add_processed_review(review['id'])
                sent_count += 1

        logger.info(
            f"Обработка завершена. Найдено {len(negative_reviews)} новых негативных отзывов, отправлено {sent_count} уведомлений")

    except Exception as e:
        logger.error(f"Критическая ошибка в основном процессе: {e}")
    finally:
        logger.info("=" * 50)
        logger.info("Проверка отзывов завершена")
        logger.info("=" * 50)


if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(main())