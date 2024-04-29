import os
import http.server
import socketserver
import aiohttp
import asyncio

from http import HTTPStatus


class Handler(http.server.SimpleHTTPRequestHandler):
    async def fetch_data(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    return data
                else:
                    return f"Request failed with status code: {response.status}"

    def do_GET(self):
        url = "https://orca-app-g3w23.ondigitalocean.app/sample/hello"
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response_data = loop.run_until_complete(self.fetch_data(url))
        loop.close()

        self.send_response(HTTPStatus.OK)
        self.end_headers()
        msg = 'Hello! You requested %s\nResponse from URL: %s' % (self.path, response_data)
        self.wfile.write(msg.encode())


port = int(os.getenv('PORT', 80))
print('Listening on port %s' % (port))
httpd = socketserver.TCPServer(('', port), Handler)
httpd.serve_forever()
