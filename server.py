import os
import http.server
import socketserver
import aiohttp
import asyncio

from http import HTTPStatus


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        msg = 'Hello! you requested %s' % (self.path)
        self.wfile.write(msg.encode())


port = int(os.getenv('PORT', 80))
print('Listening on port %s' % (port))
httpd = socketserver.TCPServer(('', port), Handler)
httpd.serve_forever()



async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.text()
                print("Response:", data)
            else:
                print(f"Request failed with status code: {response.status}")

async def main():
    url = "https://orca-app-g3w23.ondigitalocean.app/sample/hello"
    await fetch_data(url)

asyncio.run(main())
