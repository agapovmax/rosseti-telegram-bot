# rosseti_telegram_bot

# About
Telegram-бот для получения информации о плановых отключениях.

# Configure
Настройки хранятся в .config.cfg

token = токен для телеграм бота 

region = регион для поиска работ, обязательный параметр (Архангельск, Карелия, Коми и т.п)

days = количество дней для диапазона поиска

# Installation 

Требует наличия библиотеки pyTelegramBotAPI (https://github.com/eternnoir/pyTelegramBotAPI)

pip3 uninstall telebot

pip3 install PyTelegramBotAPI -U

pip3 install -U .requirements.txt

git clone https://github.com/agapovmax/rosseti-telegram-bot.git

# Running 

Для фонового запуска

nohup python3 rosseti-telegram-bot.py &

Логи в виде "Дата: Запрос: Кол-во записей" хранится в рабочей директории скрипта

# Docker-way

cd /home/user/python

git clone https://github.com/agapovmax/rosseti-telegram-bot.git

cd rosseti-telegram-bot

docker build -t rosseti-newmessage-bot .

docker run -d --restart on-failure rosseti-telegram-bot