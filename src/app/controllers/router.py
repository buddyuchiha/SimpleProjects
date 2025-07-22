import re 
from http.server import BaseHTTPRequestHandler

from app.models.models import Currencies, ExchangeRates
from app.services.logging import logger

class Router:
    def __init__(self):
        self.currencies = Currencies()
        self.exchange_rates = ExchangeRates() 
    
    def handle(self, path):
        match path:
            case "/currencies":
                logger.info(f"Router catch '/currencies' path to: {path}")
                return self.handle_currencies()
            case _ if re.fullmatch(r"/currency/\w{3}", path):
                logger.info(f"Router catch '/currency/CODE' path to: {path}")
                return self.handle_numeric_currency()
            
            case "/exchangeRates":
                logger.info(f"Router catch '/exchangeRates' path to: {path}")
                return self.handle_exchange_rates()
            case _ if re.fullmatch(r"/exchangeRate/\w{6}", path):
                logger.info(f"Router catch '/exchangeRates' path to: {path}")
                return self.handle_exchange_rate()
            
            case _ if re.fullmatch(r"/\S+", path):
                logger.info(f"Router catch default path to: {path}")
                return self.handle_home()
            
    def handle_home(self):
        logger.info(f"Calling handle_home function")
        return "<html><body><h1>HOME</h1></body></html>"
    
    def handle_currencies(self):
        logger.info(f"Calling handle_currencies function")
        return self.currencies.read()
    
    def handle_numeric_currency(self):
        logger.info(f"Calling handle_numeric_currency function")
        return "<html><body><h1>handle_numeric_currency</h1></body></html>"

    def handle_exchange_rates(self):
        logger.info(f"Calling handle_exchange_rates function")
        return self.exchange_rates.read()
    
    def handle_exchange_rate(self):
        logger.info(f"Calling handle_exchange_rate function")
        return "<html><body><h1>handle_exchange_rate</h1></body></html>"