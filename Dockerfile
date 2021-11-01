FROM python:3

WORKDIR /home/user/python/rosseti-telegram-bot

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./rosseti-telegram-bot.py" ]