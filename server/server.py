import asyncio
import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web


@aiohttp_jinja2.template('homepage.html')
async def homepage(request):
    return {}


async def initial_app():
    init_app = web.Application()
    aiohttp_jinja2.setup(init_app, loader=jinja2.FileSystemLoader("templates"))
    init_app.router.add_get("/", homepage)
    init_app.router.add_static('/static', 'templates/static')
    return init_app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(initial_app())
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, port=8080)
