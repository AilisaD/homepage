import aiohttp_jinja2
import jinja2
from aiohttp import web
import asyncio
import logging
from views import homepage


async def initial_app():
    init_app = web.Application()
    aiohttp_jinja2.setup(
        init_app,
        loader=jinja2.FileSystemLoader('templates')
    )
    init_app.router.add_get('/', homepage)
    return init_app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(initial_app())
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, port=8181)
