import json

from http.server import HTTPServer, BaseHTTPRequestHandler

from app.utils.logging import logger
from core import config
from .router import Router


class ExchangeHTTP(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server) -> None:
        self.router = Router()
        super().__init__(request, client_address, server)
    
    def set_headers(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        logger.info("Set headers")
        
    def get_json_data(self) -> dict:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        logger.info("Get JSON data")
        
        return json.loads(post_data.decode())
        
    def do_GET(self) -> None:
        self.set_headers()
        logger.info(f"GET Request with path: {self.path}")
        
        answer = self.router.handle_get(self.path)
        
        logger.info(
            f"Answer to GET Request with path"
            f"{self.path}: {json.dumps(answer)}"
            )
        
        self.wfile.write(json.dumps(answer).encode('utf-8'))             
        
    def do_POST(self):
        data = self.get_json_data()
        self.set_headers()
        
        logger.info(f"POST Request with path: {self.path} and data: {data}")
        answer = self.router.handle_post(self.path, data)
        
        logger.info(
            f"Answer to POST Request with path"
            f"{self.path}: {json.dumps(answer)}"
            )
        
        self.wfile.write(json.dumps(answer).encode('utf-8')) 
        
    def do_PATCH(self):
        data = self.get_json_data()
        self.set_headers()
        
        logger.info(f"PATCH Request with path: {self.path} and data: {data}")
        answer = self.router.handle_patch(self.path, data)
        
        logger.info(
            f"Answer to PATCH Request with path"
            f"{self.path}: {json.dumps(answer)}"
            )
        
        self.wfile.write(json.dumps(answer).encode('utf-8')) 
             


def start():
    logger.info(
        f"Creating server with HOST: {config.HOST}, PORT: {config.PORT}."
        )
    server = HTTPServer((config.HOST, config.PORT), ExchangeHTTP)
    server.serve_forever()
    server.server_close
    logger.info(
        f"Server closed with HOST: {config.HOST}, PORT: {config.PORT}."
        )