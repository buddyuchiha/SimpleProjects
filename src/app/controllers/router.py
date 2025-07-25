import re 
from http.server import BaseHTTPRequestHandler

from app.models.models import Currencies, ExchangeRates
from app.utils.logging import logger

class Router:
    def __init__(self) -> None:
        self.currencies = Currencies()
        self.exchange_rates = ExchangeRates() 
    
    def handle_get(self, path: str) -> dict:
        logger.info(f"Entered in GET handler with path: {path}")
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
                logger.info(f"Router catch '/exchangeRate/PAIR' path to: {path}")
                return self.handle_exchange_rate(path)
            
            case _ if re.fullmatch(r"/\S+", path):
                logger.info(f"Router catch default path to: {path}")
                return self.handle_home()
                
    def handle_post(self, path: str, data: str) -> dict:
        logger.info(
            f"Entered in POST handler with path: {path} and data: {data}"
            )
        match path:
            case "/currencies":
                logger.info(f"Router catch '/currencies' path to: {path}")
                return self.handle_currencies_data(data)
            case "/exchangeRates":
                logger.info(
                    f"Router catch '/exchangeRates' path to: {path}"
                    )
                return self.handle_exchange_rates_data(data)
                
    def handle_patch(self, path: str, data: dict) -> None: 
        logger.info(
            f"Entered in PATCH handler with path: {path} and data: {data}"
            )
        match path:    
            case _ if re.fullmatch(r"/exchangeRate/\w{6}", path):
                logger.info(f"Router catch '/exchangeRate/PAIR' path to: {path}")
                return self.handle_update_exchange_rate(path, data) 
            
    def handle_home(self):
        logger.info(f"Calling handle_home function")
        return "<html><body><h1>HOME</h1></body></html>"
    
    def handle_currencies(self) -> dict:
        answer = self.currencies.read()
        
        logger.info(
            f"Calling handle_currencies function and received: {answer}"
            )
        
        return answer
    
    def handle_numeric_currency(self, path: str) -> dict:
        code = path[-3:]
        answer = self.currencies.read_row(code)
        
        logger.info(
            f"Calling handle_numeric currency function"
            f"and received: {answer} for code: {code}"
            )
        
        return answer
    
    def handle_exchange_rates(self) -> dict:
        answer = self.exchange_rates.read()
        
        logger.info(
            f"Calling handle_exchange_rates function and received: {answer}"
            )
        
        return answer
    
    def handle_exchange_rate(self, path: str) -> dict:
        first_code = path[-6:-3]
        second_code = path[-3:]
        answer = self.exchange_rates.read_row(first_code, second_code) 
        
        logger.info(
            f"Calling handle_exchange_rate function and received: {answer}")
        
        return answer
    
    def handle_currencies_data(self, data: dict) -> None:
        logger.info(
            f"Calling handle_currencies_data function for "
            f"name: {data["name"]}, code: {data["code"]},"
            f"sign: {data["sign"]}"
            )
        
        self.currencies.create(data["name"], data["code"], data["sign"]) 
    
    def handle_exchange_rates_data(self, data: dict) -> None:
        logger.info(
            f"Calling handle_exchange_rates_data function for "
            f"base_currency_id: {data["base_currency_id"]},"
            f"target_currency_id: {data["target_currency_id"]},"
            f"rate: {data["rate"]}"
            )
        
        self.exchange_rates.create(
            data["base_currency_id"],
            data["target_currency_id"],
            data["rate"]
        )
        
    def handle_update_exchange_rate(self, path: str, data: dict) -> dict: 
        first_code = path[-6:-3]
        second_code = path[-3:]
        answer = self.exchange_rates.update(first_code, second_code, data["rate"]) 
        
        logger.info(
            f"Calling handle_update_exchange_rate function"
            f"for rate: {data["rate"]} and received: {answer}"
            )

        return answer