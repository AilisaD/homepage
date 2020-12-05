import asyncio
import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web

import requests
import json
from datetime import datetime as dt

dict_weather = {
    'clear': 'ясно',
    'partly-cloudy': 'малооблачно',
    'cloudy': 'облачно с прояснениями',
    'overcast': 'пасмурно',
    'drizzle': 'морось',
    'light-rain': 'небольшой дождь',
    'rain': 'дождь',
    'moderate-rain': 'умеренно сильный дождь',
    'heavy-rain': 'сильный дождь',
    'continuous-heavy-rain': 'длительный сильный дождь',
    'showers': 'ливень',
    'wet-snow': 'дождь со снегом',
    'light-snow': 'небольшой снег',
    'snow': 'снег',
    'snow-showers': 'снегопад',
    'hail': 'град',
    'thunderstorm': 'гроза',
    'thunderstorm-with-rain': 'дождь с грозой',
    'thunderstorm-with-hail': 'гроза с градом',
}


@aiohttp_jinja2.template("homepage.html")
async def homepage(request):
    return {}


async def initial_app():
    init_app = web.Application()
    aiohttp_jinja2.setup(init_app, loader=jinja2.FileSystemLoader("templates"))
    init_app.router.add_get("/", homepage)
    init_app.router.add_static("/static", "templates/static")
    return init_app


def get_weather():
    """https://api.weather.yandex.ru/v1/informers?lat=55.81370&lon=37.36522"""
    response = requests.get(
        "https://api.weather.yandex.ru/v1/informers?lat=55.81370&lon=37.36522",
        headers={
            'Content-type': 'text/html',
            'X-Yandex-API-Key': 'b93b02b0-da03-4600-9a9c-d396d249fd5b'},
    )
    weather = json.loads(response.text)
    time = dt.fromtimestamp(weather['fact']['obs_time']).strftime("%H:%M")
    temperature = weather['fact']['temp']
    if weather['fact']['temp'] > 0:
        temperature = '+' + str(temperature)
    condition = dict_weather[weather['fact']['condition']]
    # print(time, temperature, condition)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(initial_app())
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, port=8080)
