import requests
import telebot
import datetime
import re
import config

# Берем с конфига token для бота
conf = config.Config('config.cfg')
bot = telebot.TeleBot(conf['token'])
# Берем из конфига кол-во дней для диапазона выдачи с и по
days = conf['days']
# Задаем регион для поиска работ
region = conf['region']

url = 'https://lk.mrsksevzap.ru/Ajax/Interruptions?region=&district=&settlement=&isSettlement=true&manualSettlement=&street=&isManualStreet=true&manualStreet=&house=&page=1&fieldName=OutageDate&orderDirection=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Введите название города\песелка\деревни")

@bot.message_handler(content_types=['text'])
def start_command(message):
    # Проверяем текст на наличие только русских букв. Иначе выводим сообщение об ошибке
    if has_cyrillic(message.text):
        # Вывод дат в нужном диапазоне в неделю 
        fulltime = datetime.datetime.now()
        currdate = datetime.datetime.today()
        todate = (datetime.datetime.today()).strftime("%d.%m.%Y")
        fromdate = (currdate - datetime.timedelta(days=int(days))).strftime("%d.%m.%Y")
        params = {
                'fullAddress': message.text,
                'region': region,
                'district':'',
                'settlement':'',
                'isSettlement': 'true',
                'from': fromdate,
                'to': todate,
            }
        r = requests.get(url, headers=headers, params = params)
        a = r.json()
        # Считаем, сколько запланировано работ
        count = a.get('TotalCount')
        # Пишем в файл данные
        # Открываем лог файл для записи
        f = open('rosseti-telegram-log.txt', 'a')
        print("Запрос по: " + message.text)
        print("Количество записей " + str(count) + '\n')
        f.write(str(fulltime) + '; ' + message.text + '; ' + str(count) + '\n')
        f.close()
        # Если по данному запросу нет работ (их 0)
        if count == 0 :
            result = ('В ' + message.text + ' с ' + fromdate + ' по ' + todate + ' никаких работ не запланировано' + '\n')
            result += ("Уточните информацию по телефону 8 (800) 220-0-220" + '\n')
            result += ("Если отключение аварийное - создайте обращение на портале Светлая Страна https://xn--80aaafp0bqweeid1o.xn--p1ai/platform/portal/cons_main" + "\n")
            result += ("или на официальном сайте Россети Северо-Запад https://lk.mrsksevzap.ru/Appeal/OutageAppeal")
            bot.send_message(message.chat.id, result)
        else:
            for item in a['items']:
                result = ( item['Description'] + ' отключение по адресу ' + item['Address'] + ' c ' + item['From'] + ' по ' + item['To'] + ' ' + item['Condition'])
                bot.send_message(message.chat.id, result)
    else:
        result = "Ошибка! Название следует писать русскими буквами!"
        bot.send_message(message.chat.id, result)
bot.polling(none_stop = True)