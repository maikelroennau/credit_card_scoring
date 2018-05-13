#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer


class CreditCardScoring(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()


    def do_GET(self):
        self._set_headers()
        self.wfile.write("json")
        # Send infrastructure information


    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        # Validate input
        # Run accordingly
        #   Predict
        #   Train model
        #   Update model

        self._set_headers()
        self.wfile.write('{"id": "8db4206f-8878-174d-7a23-dd2c4f4ef5a0", "prediction": 0.1495 }')


def run(server_class=HTTPServer, handler_class=CreditCardScoring, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print("Starting server...")
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
