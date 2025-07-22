import json

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

from app.services.logging import logger
from core import config
from .router import Router


class ExchangeHTTP(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.router = Router()
        super().__init__(request, client_address, server)
        
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        logger.info(f"GET Request with path: {self.path}")
        answer = self.router.handle(self.path)
        self.wfile.write(json.dumps(answer).encode('utf-8'))        
        # self.wfile.write(bytes("<html><body><h1>HELLO WORLD</h1></body></html>", "utf-8"))        
        
    def do_POST(self):
        pass

def start():
    logger.info(f"Creating server with HOST: {config.HOST}, PORT: {config.PORT}.")
    server = HTTPServer((config.HOST, config.PORT), ExchangeHTTP)
    server.serve_forever()
    server.server_close
    logger.info(f"Server closed with HOST: {config.HOST}, PORT: {config.PORT}.")