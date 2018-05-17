#!/usr/bin/env python
"""
Send a POST request::
    curl -d '{"id": "8db4206f-8878-174d-7a23-dd2c4f4ef5a0", "score_3": 480.0, "score_4": 105.2, "score_5": 0.8514, "score_6": 94.2, "income": 500000}' localhost:8080
    Using port '8080' so it won't conflict with any other service
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

from model import predict, load_model, save_prediction
from constants import *
import json

from multiprocessing import Process


class CreditCardScoring(BaseHTTPRequestHandler):
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


    def do_GET(self):
        self._set_headers()
        self.wfile.write("json")
        # Send infrastructure information


    def do_HEAD(self):
        self._set_headers()


    def do_POST(self):
        self._set_headers()
        # Read input
        self.data_input = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        # Converting data to JSON and getting a prediction
        data = json.loads(self.data_input)
        prediction = predict(load_model(), data)

        # Building JSON response
        response = {}
        response["id"] = data["id"]
        response["prediction"] = prediction

        self.wfile.write(json.dumps(response))

        save_prediction(response)


def run(server_class=HTTPServer, handler_class=CreditCardScoring, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print("Server running on port {}".format(port))
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
