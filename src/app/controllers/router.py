import re 
from http.server import BaseHTTPRequestHandler

from app.models.models import Currencies, ExchangeRates
from app.services.logging import logger

class Router:
    def __init__(self):
        self.currencies = Currencies()
        self.exchange_rates = ExchangeRates() 
    
    def handle_get(self, path: str) -> dict:
        match path:
            case "/currencies":
                logger.info(f"Router catch '/currencies' path to: {path}")
                return self.handle_currencies()
            case _ if re.fullmatch(r"/currency/\w{3}", path):
                logger.info(f"Router catch '/currency/CODE' path to: {path}")
                return self.handle_numeric_currency(path)
            
            case "/exchangeRates":
                logger.info(f"Router catch '/exchangeRates' path to: {path}")
                return self.handle_exchange_rates()
            case _ if re.fullmatch(r"/exchangeRate/\w{6}", path):
                logger.info(f"Router catch '/exchangeRates' path to: {path}")
                return self.handle_exchange_rate()
            
            case _ if re.fullmatch(r"/\S+", path):
                logger.info(f"Router catch default path to: {path}")
                return self.handle_home()
                
    def handle_post(self, path: str, data: str) -> None:
            match path:
                case "/currencies":
                    logger.info(f"Router catch '/currencies' path to: {path}")
                    return self.handle_currencies_data(data)
                case "/exchangeRates":
                    logger.info(
                        f"Router catch '/exchangeRates' path to: {path}"
                        )
                    return self.handle_exchange_rates()
                
    def handle_home(self):
        logger.info(f"Calling handle_home function")
        return "<html><body><h1>HOME</h1></body></html>"
    
    def handle_currencies(self):
        answer = self.currencies.read()
        logger.info(
            f"Calling handle_currencies function and received: {answer}"
            )
        return answer
    
    def handle_numeric_currency(self, path: str):
        code = path[-3:]
        answer = self.currencies.read_row(code)
        logger.info(
            f"Calling handle_currencies function"
            f"and received: {answer} for code: {code}"
            )
        return answer
    
    def handle_exchange_rates(self):
        logger.info(f"Calling handle_exchange_rates function")
        return self.exchange_rates.read()
    
    def handle_exchange_rate(self):
        logger.info(f"Calling handle_exchange_rate function")
        return "<html><body><h1>handle_exchange_rate</h1></body></html>"
    
    def handle_currencies_data(self, data: dict):
        logger.info(
            f"Calling handle_currencies_data function for "
            f"name: {data["name"]}, code: {data["code"]},"
            f"sign: {data["sign"]}"
            )
        self.currencies.create(data["name"], data["code"], data["sign"]) 
    
        