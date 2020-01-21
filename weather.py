import telebot
import time
from bs4 import BeautifulSoup
import requests

bot = telebot.TeleBot('934119066:AAHSxlgxljwjZYT88lL2d7JOby_MfIc27ec')

html_response = requests.get('https://yandex.ru/pogoda/staraya-russa')
soup = BeautifulSoup(html_response.text, 'lxml')

while True:

    search_parsing = soup.find('div', class_="temp fact__temp fact__temp_size_s").find('span', class_='temp__value')
    print(search_parsing)

    base = open('temperature.txt', 'r')
    base.seek(0)
    readed_base = base.read()
    base.close()
    print(readed_base)
    if search_parsing.text == readed_base:
        bot.send_message(543176947, 'РџРѕРіРѕРґР° РЅРµ РёР·РјРµРЅРёР»Р°СЃСЊ:) ')
    else:
        bot.send_message(543176947, 'СЃРµР№С‡Р°СЃ РЅР° СѓР»РёС†Рµ: ' + search_parsing.text)
        base = open('temperature.txt', 'w')
        base.seek(0)
        base.write(search_parsing.text)
        base.close()

    time.sleep(3600)
bot.polling()
