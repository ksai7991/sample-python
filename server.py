import os
import aiohttp
from aiohttp import web
import asyncio
import socket

async def handle(request):
    # Making a request to the specified endpoint
    async with aiohttp.ClientSession() as session:
        async with session.get('https://faas-blr1-8177d592.doserverless.co/api/v1/web/fn-100bea51-4ace-4d4f-bd57-ec37b1664387/default/python',
                               headers={"Content-Type": "application/json", "X-Require-Whisk-Auth": "Ne7r8kmzYl0wswE"}) as response:
            if response.status == 200:
                response_content = await response.text()
            else:
                response_content = "Failed to fetch response from endpoint"

    # Get the hostname
    hostname = socket.gethostname()

    # Appending the response content and hostname to the message
    msg = f'Hello! You requested {request.path}. Response from endpoint: {response_content}. Hostname: {hostname}'
    return web.Response(text=msg)

async def delayed_startup(app):
    await asyncio.sleep(1)  # Delay server startup by 2 minutes
    print("Server startup delayed by 2 minutes")

port = int(os.getenv('PORT', 8080))

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)

# Register delayed startup coroutine
app.on_startup.append(delayed_startup)

web.run_app(app, port=port)
