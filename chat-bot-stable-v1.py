import requests
import telebot

bot = telebot.TeleBot("1981156863:AAEQYO0P8iw8_nsmPO_O7FTF9ImgY1Xej_Y")
url = 'https://lk.mrsksevzap.ru/Ajax/Interruptions?region=&district=&settlement=&isSettlement=true&manualSettlement=&street=&isManualStreet=true&manualStreet=&house=&page=1&fieldName=OutageDate&orderDirection=1'
#url = 'https://clients.mrsksevzap.ru/powertransmission/poweroutage/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

@bot.message_handler(content_types=['text'])
def start_command(message):
        
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
            'from': '01.09.2021',
            'to': '15.09.2021',
            #'page': '1',
            #'PageSize': '40',
            #'fieldName': 'OutageDate',
            #'orderDirection': '1'
        }
    r = requests.get(url, headers=headers, params = params)
    # print(r.url)
    a = r.json()
    print(a)
    print(type(a))
    count = a.get('TotalCount')
    print(count)
    if count == 0 :
        result = ('В ' + message.text + ' никаких работ не запланировано')
        bot.send_message(message.chat.id, result)
    else:
    #print(a['items'])
        for item in a['items']:
            result = ( item['Description'] + ' отключение по адресу ' + item['Address'] + ' c ' + item['From'] + ' по ' + item['To'] + ' ' + item['Condition'] + '\n\n')
        #print(result)
        #print(type(result))
        #result += result 
    #else result == 'Пусто'
            #print(result)
            bot.send_message(message.chat.id, result)
bot.polling(none_stop= True)

# TODO
# Добавить проверку если нет плановых работ, иначе скрипт валится
# Сделать полный вывод переменной result, а не последнее значение
# 