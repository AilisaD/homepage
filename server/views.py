import aiohttp_jinja2


@aiohttp_jinja2.template('homepage.html')
async def homepage(request):
    return {}
