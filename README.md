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
# Запуск бота каждый день/месяц/год раз в два часа с 9 до 19 часов
0 9,11,13,15,17,19 * * * /home/root/review_alert/venv/bin/python /home/root/review_alert/main.py >> /home/root/review_alert/logs/cron.log 2>&1

# Очистка крон лога каждый понедельник в 0:00 до 2000 строк
0 0 * * 1 tail -n 2000 /home/root/review_alert/logs/cron.log > /home/root/review_alert/logs/cron.log.tmp && mv /home/root/review_alert/logs/cron.log.tmp /home/root/review_alert/logs/cron.log

# Очистка бот лога каждый понедельник в 0:00 до 2000 строк
0 0 * * 1 tail -n 2000 /home/root/review_alert/logs/bot.log > /home/root/review_alert/logs/bot.log.tmp && mv /home/root/review_alert/logs/bot.log.tmp /home/root/review_alert/logs/bot.log

# Напоминание об обновление системного гайда
0 0 1 * * sed -i "s/Последнее обновление: .*/Последнее обновление: $(date)/" /home/iskan_der/system_services_guide.md
