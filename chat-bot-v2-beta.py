import requests
import telebot
import datetime
import re

bot = telebot.TeleBot("1981156863:AAEQYO0P8iw8_nsmPO_O7FTF9ImgY1Xej_Y")
url = 'https://lk.mrsksevzap.ru/Ajax/Interruptions?region=&district=&settlement=&isSettlement=true&manualSettlement=&street=&isManualStreet=true&manualStreet=&house=&page=1&fieldName=OutageDate&orderDirection=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }


def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

# Вывод дат в нужном диапазоне в неделю 
currdate = datetime.datetime.today()
todate = (datetime.datetime.today()).strftime("%d.%m.%Y")
fromdate = (currdate - datetime.timedelta(days=7)).strftime("%d.%m.%Y")
# Открываем лог файл для записи
f = open('chat-bot-log.txt', 'a')
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Введите название города\песелка\деревни")

@bot.message_handler(content_types=['text'])
def start_command(message):
    # Проверяем текст на наличие только русских букв. Иначе выводим сообщение об ошибке
    if has_cyrillic(message.text):

        params = {
                #'manualRegion': 'Карелия', 
                'fullAddress': message.text,
                'region':'',
                'district':'',
                'settlement':'',
                'isSettlement': 'true',
                #'manualSettlement':'',
                #'street':'',
                #'isManualStreet':'',
                #'manualStreet':'',
                #'house':'',
                'from': fromdate,
                'to': todate,
                #'page': '1',
                #'PageSize': '40',
                #'fieldName': 'OutageDate',
                #'orderDirection': '1'
            }
        r = requests.get(url, headers=headers, params = params)
        a = r.json()
        # Считаем, сколько запланировано работ
        count = a.get('TotalCount')
        # Пишем в файл данные
        print("Запрос по: " + message.text)
        print("Количество записей " + str(count) + '\n')
        fdata = f.write('Запрос по: ' + message.text + 'количество записей ' + str(count) + '\n')
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
f.close()

# TODO
# Запись логов в файл
# Отдельный файл с id чат бота
# 