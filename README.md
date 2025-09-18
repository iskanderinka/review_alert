Структура проекта

review_alert/
│
├── config.py          # Конфиги: токен бота, chat_id, URL сайта и т.д.
├── storage.py         # Вся работа с базой данных
├── parser.py          # Логика парсинга сайта
├── bot.py             # Логика работы Telegram-бота
├── main.py            # Главный файл, который всё запускает
├── logger.py          # Собираем логи
├── requirements.txt   # Список зависимостей (библиотек)
├── logs/              # Папка для логов (создастся автоматически)
└── .env               # Файл для конфиденциальных данных



Обнови список зависимостей для будущей работы
pip freeze > requirements.txt

Так обновить сама зависимости перед работой
pip install -r requirements.txt


crontab -e
# Запуск бота каждый день/месяц/год раз в час с 9 до 19 часов
0 9-19 * * * /usr/bin/python3 /root/review_alert/main.py >> /root/review_alert/logs/cron.log 2>&1

# Очистка лога каждое воскресенье в 0:00 до 500 строк
0 0 * * 0 tail -n 500 /root/review_alert/logs/cron.log > /root/review_alert/logs/cron.log.tmp && mv /root/review_alert/logs/cron.log.tmp /root/review_alert/logs/cron.log