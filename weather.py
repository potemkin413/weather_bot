import aiogram
import time
from bs4 import BeautifulSoup
import requests
import asyncio
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

dayly_list  = []
bot = aiogram.Bot(token='934119066:AAHSxlgxljwjZYT88lL2d7JOby_MfIc27ec')
dp = aiogram.Dispatcher(bot)


html_response = requests.get('https://yandex.ru/pogoda/staraya-russa')
soup = BeautifulSoup(html_response.text, 'html.parser')
day_parsing = soup.find('div', class_="b-page__container").find('div', class_="content__row content__row_with-right-margin").find('ul', class_="swiper-wrapper")



async def one_time_forecast():

    while True:
        html_response = requests.get('https://yandex.ru/pogoda/staraya-russa')
        soup = BeautifulSoup(html_response.text, 'html.parser')
        search_parsing = soup.find('div', class_="temp fact__temp fact__temp_size_s").find('span', class_='temp__value')
        await bot.send_message(chat_id=543176947, text='Температура в данный момент: ' + search_parsing.text)
        await asyncio.sleep(3600)


def user_request():
    @dp.message_handler(commands=['30days🌦'])
    async def weather_parsing(message):

        button_city = KeyboardButton('/30days🌦')

        greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        greet_kb.add(button_city)

        weather = []
        name_day = [days.text for days in day_parsing.find_all('div', class_='forecast-briefly__name')]
        number_day = [days.text for days in day_parsing.find_all('time', class_='time forecast-briefly__date')]
        temperature = [temp.text for temp in
                       day_parsing.find_all('div', class_='temp forecast-briefly__temp forecast-briefly__temp_day')]
        weather.append(name_day)
        weather.append(number_day)
        weather.append(temperature)
        for i in range(len(name_day)):
            list_weather = f'{name_day[i]} {number_day[i]} {temperature[i]}'
            await message.reply(list_weather, reply_markup=greet_kb)

async def main():
    asyncio.create_task(one_time_forecast())
    user_request()
    await dp.start_polling()

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())

