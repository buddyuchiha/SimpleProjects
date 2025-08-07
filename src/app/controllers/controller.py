import json
from http.server import HTTPServer, BaseHTTPRequestHandler

from app.models.models import Currencies, ExchangeRates
from app.utils.exceptions import (
    BadRequest400,
    Conflict409, 
    NotFound404, 
    ServerError500
)
from app.utils.logging import logger
from app.utils.services import ServiceConverted
from core.config import config
from .router import Router


class ExchangeHTTP(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server) -> None:
        currencies = Currencies()
        exchange_rates = ExchangeRates()
        service = ServiceConverted()
        
        self.router = Router(currencies, exchange_rates, service)
        super().__init__(request, client_address, server)
    
    def set_headers(self, code: int = 200) -> None:
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        logger.info("Set headers")
        
    def get_json_data(self) -> dict:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        logger.info("Get JSON data")
        
        return json.loads(post_data.decode())

    def send_mistake(self, code: int, e: object) -> None:
        self.send_response(code)
        self.end_headers()
        self.wfile.write(json.dumps(e.to_dict()).encode('utf-8'))

    def do_GET(self) -> None: 
        try:
            self.set_headers()
            logger.info(f"GET Request with path: {self.path}")
            
            answer = self.router.handle_get(self.path)
            
            logger.info(
                f"Answer to GET Request with path "
                f"{self.path}: {answer}"
                )
            
            self.wfile.write(json.dumps(answer).encode('utf-8')) 
              
        except ServerError500 as e:
           self.send_mistake(500, e)
            
        except BadRequest400 as e:
            self.send_mistake(400, e)
     
        except NotFound404 as e:
            self.send_mistake(404, e)
                     
    def do_POST(self) -> None:
        try:
            data = self.get_json_data()
            self.set_headers(201)
            
            logger.info(
                f"POST Request with path: {self.path} and data: {data}"
                )
            answer = self.router.handle_post(self.path, data)
            
            logger.info(
                f"Answer to POST Request with path"
                f"{self.path}: {json.dumps(answer)}"
                )
            
            self.wfile.write("POST request handled".encode('utf-8')) 
               
        except ServerError500 as e:
            self.send_mistake(500, e)
            
        except BadRequest400 as e:
            self.send_mistake(400, e)
            
        except NotFound404 as e:
            self.send_mistake(404, e)
            
        except Conflict409 as e:
            self.send_mistake(409, e)
            
    def do_PATCH(self) -> None:
        try:
            data = self.get_json_data()
            self.set_headers()
            
            logger.info(
                f"PATCH Request with path: {self.path} and data: {data}"
                )
            answer = self.router.handle_patch(self.path, data)
            
            logger.info(
                f"Answer to PATCH Request with path"
                f"{self.path}: {json.dumps(answer)}"
                )
            
            self.wfile.write("PATCH request handled".encode('utf-8')) 
             
        except ServerError500 as e:
            self.send_mistake(500, e)

        except BadRequest400 as e:
            self.send_mistake(400, e)
            
        except NotFound404 as e:
            self.send_mistake(404, e)
            
        except Conflict409 as e:
            self.send_mistake(409, e)


def start() -> None:
    logger.info(
        f"Creating server with HOST: {config['SERVER']['HOST']}, "
        f"PORT: {config['SERVER']['PORT']}."
        )
    
    server = HTTPServer(
        (config['SERVER']['HOST'], config['SERVER']['PORT']),
        ExchangeHTTP
        )
    server.serve_forever()
    server.server_close()
    
    logger.info(
        f"Server closed with HOST: {config['SERVER']['HOST']}, "
        f"PORT: {config['SERVER']['PORT']}."
        )