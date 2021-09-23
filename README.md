# mrsk_bot

Telegram-бот для получения информации о плановых отключениях.
Настройки хранятся в config.cfg
    token = токен для телеграм бота 
    region = регион для поиска работ, обязательный параметр (Архангельск, Карелия, Коми и т.п)
    days = количество дней для диапазона поиска

Требует наличия библиотеки pyTelegramBotAPI (https://github.com/eternnoir/pyTelegramBotAPI)
pip3 uninstall telebot
pip3 install PyTelegramBotAPI -U

Для фонового запуска
python3 chat-bot.py &

Логи в виде "Дата: Запрос: Кол-во записей" хранится в рабочей директории скрипта 