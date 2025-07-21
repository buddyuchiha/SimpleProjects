from http.server import HTTPServer, BaseHTTPRequestHandler

from app.services.logging import logger
from core import config

class ExchangeHTTP(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        self.wfile.write(bytes("<html><body><h1>HELLO WORLD</h1></body></html>", "utf-8"))        

    def do_POST(self):
        pass

def start():
    logger.info(f"Creating server with HOST: {config.HOST}, PORT: {config.PORT}.")
    server = HTTPServer((config.HOST, config.PORT), ExchangeHTTP)
    server.serve_forever()
    server.server_close
    logger.info("")