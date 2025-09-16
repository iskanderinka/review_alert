from storage import load_processed_reviews, add_processed_review
from parser import get_reviews
from bot import send_telegram_alert
from logger import logger


def main():
    """
    Основная функция приложения.
    Запускает процесс проверки отзывов и отправки уведомлений.
    """
    logger.info("=" * 50)
    logger.info("Запуск проверки отзывов")
    logger.info("=" * 50)

    try:
        # Загружаем ID уже обработанных отзывов
        processed_reviews = load_processed_reviews()
        logger.info(f"Загружено {len(processed_reviews)} обработанных отзывов")

        # Получаем новые отзывы с сайта
        reviews = get_reviews()

        if not reviews:
            logger.warning("Не удалось получить отзывы или список пуст")
            # Сохраняем факт пустого ответа для мониторинга
            with open('last_run.txt', 'w') as f:
                f.write("empty")
            return

        # Сохраняем факт успешного получения отзывов
        with open('last_run.txt', 'w') as f:
            f.write(f"success_{len(reviews)}")

        # Фильтруем отзывы: оставляем только негативные и новые
        negative_reviews = []
        for review in reviews:
            # Пропускаем уже обработанные отзывы
            if review['id'] in processed_reviews:
                logger.debug(f"Отзыв {review['id']} уже обработан, пропускаем")
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
            success = send_telegram_alert(review)
            if success:
                # Помечаем отзыв как обработанный только после успешной отправки
                add_processed_review(review['id'])
                sent_count += 1

        logger.info(
            f"Обработка завершена. Найдено {len(negative_reviews)} новых негативных отзывов, отправлено {sent_count} уведомлений")

    except Exception as e:
        logger.error(f"Критическая ошибка в основном процессе: {e}")
        # Сохраняем факт ошибки
        with open('last_run.txt', 'w') as f:
            f.write(f"error_{str(e)}")
    finally:
        logger.info("=" * 50)
        logger.info("Проверка отзывов завершена")
        logger.info("=" * 50)


if __name__ == "__main__":
    main()