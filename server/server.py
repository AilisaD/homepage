import asyncio
import logging
import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

import requests
import json
from datetime import datetime as dt


dict_weather = {
    "clear": "ясно",
    "partly-cloudy": "малооблачно",
    "cloudy": "облачно с прояснениями",
    "overcast": "пасмурно",
    "drizzle": "морось",
    "light-rain": "небольшой дождь",
    "rain": "дождь",
    "moderate-rain": "умеренно сильный дождь",
    "heavy-rain": "сильный дождь",
    "continuous-heavy-rain": "длительный сильный дождь",
    "showers": "ливень",
    "wet-snow": "дождь со снегом",
    "light-snow": "небольшой снег",
    "snow": "снег",
    "snow-showers": "снегопад",
    "hail": "град",
    "thunderstorm": "гроза",
    "thunderstorm-with-rain": "дождь с грозой",
    "thunderstorm-with-hail": "гроза с градом",
    "overcast-and-snow": "пасмурно со снегом",
    "overcast-and-light-snow": "пасмурно и небольшой снег",
}

dict_parts_name = {
    "night": "ночь",
    "morning": "утро",
    "day": "день",
    "evening": "вечер",
}


async def homepage(request):
    with open("templates/homepage.html") as f:
        text = f.read()
    return web.Response(text=text, content_type="text/html")


async def weather(request):
    fact, forecast = None, None
    if "API_token" in os.environ:
        fact, forecast = await get_weather()
    return web.json_response({"fact": fact, "forecast": forecast})


async def initial_app():
    init_app = web.Application()
    aiohttp_jinja2.setup(init_app, loader=jinja2.FileSystemLoader("templates"))
    init_app.router.add_get("/", homepage)
    init_app.router.add_get("/weather", weather)
    init_app.router.add_static("/static", "templates/static")
    return init_app


async def get_weather():
    """https://api.weather.yandex.ru/v1/informers?lat=55.81370&lon=37.36522"""
    response = requests.get(
        "https://api.weather.yandex.ru/v1/informers?lat=55.81370&lon=37.36522",
        headers={
            'Content-type': 'text/html',
            'X-Yandex-API-Key': os.getenv('API_token')},
    )
    weather_res = json.loads(response.text)
    logging.info("get_weather")
    time = dt.fromtimestamp(weather_res["fact"]["obs_time"]).strftime("%H:%M")
    temperature = weather_res["fact"]["temp"]
    temp_like = weather_res["fact"]["feels_like"]
    if weather_res["fact"]["temp"] > 0:
        temperature = "+" + str(temperature)
    if weather_res["fact"]["feels_like"] > 0:
        temp_like = "+" + str(temp_like)
    condition = dict_weather[weather_res["fact"]["condition"]]
    svg = f'https://yastatic.net/weather/i/' \
          f'icons/blueye/color/svg/{weather_res["fact"]["icon"]}.svg'
    fact = [time, temperature, temp_like, condition, svg]

    forecast = []
    for part in weather_res["forecast"]["parts"]:
        svg = f'https://yastatic.net/weather/i' \
              f'/icons/blueye/color/svg/{part["icon"]}.svg'
        t_min = part["temp_min"]
        t_max = part["temp_max"]
        if part["temp_min"] > 0:
            t_min = "+" + str(t_min)
        if part["temp_max"] > 0:
            t_max = "+" + str(t_max)
        forecast.append([
            dict_parts_name[part["part_name"]],
            t_min,
            t_max,
            dict_weather[part["condition"]],
            svg,
        ])
    return fact, forecast


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(initial_app())
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, port=8080)
