import os
import aiohttp
from aiohttp import web

async def handle(request):
    # Making a request to the specified endpoint
    async with aiohttp.ClientSession() as session:
        async with session.get('https://faas-blr1-8177d592.doserverless.co/api/v1/web/fn-100bea51-4ace-4d4f-bd57-ec37b1664387/default/python',
                               headers={"Content-Type": "application/json", "X-Require-Whisk-Auth": "Ne7r8kmzYl0wswE"}) as response:
            if response.status == 200:
                response_content = await response.text()
            else:
                response_content = "Failed to fetch response from endpoint"

    # Appending the response content to the message
    msg = f'Hello! you requested {request.path}. Response from endpoint: {response_content}'
    return web.Response(text=msg)

port = int(os.getenv('PORT', 8080))

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)

web.run_app(app, port=port)
