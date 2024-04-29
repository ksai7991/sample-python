import os
import http.server
import socketserver
import requests

from http import HTTPStatus


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Making a request to the specified endpoint
        endpoint = 'https://orca-app-g3w23.ondigitalocean.app/sample/hello'
        response = requests.get(endpoint)
        
        # Checking if the request was successful
        if response.status_code == 200:
            # Extracting the response content
            response_content = response.text
        else:
            response_content = "Failed to fetch response from endpoint"

        self.send_response(HTTPStatus.OK)
        self.end_headers()
        
        # Appending the response content to the message
        msg = 'Hello! you requested %s. Response from endpoint: %s' % (self.path, response_content)
        self.wfile.write(msg.encode())


port = int(os.getenv('PORT', 80))
print('Listening on port %s' % (port))
httpd = socketserver.TCPServer(('', port), Handler)
httpd.serve_forever()
