import config
from aiohttp import web
from balance import VirtualServerQueue
import asyncio
import json
import aiohttp_cors

@asyncio.coroutine
def handle(request):
    VirtualServerQueue.updateStats(-1)
    text = yield from VirtualServerQueue.requestService()
    return web.Response(text=text)

@asyncio.coroutine
def getservers(request):
    return web.Response(text="{'n': " + str(config.servercount) + "}")

@asyncio.coroutine
def stats(request):
    print(request.query['id'])
    vm_id = int(request.query['id']) - 1
    return web.Response(text=VirtualServerQueue.updateStats(vm_id))
    # return web.Response(text=text)

app = web.Application()

app.router.add_get('/', handle)
app.router.add_get('/stats', stats)
app.router.add_get('/numservers', getservers)


web.run_app(app)