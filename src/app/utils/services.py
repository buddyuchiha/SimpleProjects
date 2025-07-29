import re

from app.utils.dto import ConvertValueDTO
from app.utils.logging import logger
from app.models.models import Currencies, ExchangeRates


class Service:
    def __init__(self) -> None:
        self.currencies = Currencies()
        self.exchange_rates = ExchangeRates()
        
    def __get_rate(self, exchange_rates: ConvertValueDTO) -> int:
        exchange_rate = self.exchange_rates.read_row(exchange_rates)
        
        return exchange_rate[0]["rate"]
    
    @staticmethod
    def parse_coords(path) -> tuple[str | int]:
        codes = re.findall(r"=\D{3}", path)
        codes = [code[1:] for code in codes]
        
        base_currency_id = codes[0]
        target_currency_id = codes[1]
        
        amount = re.findall(r"=\d+", path)
        amount = int(amount[0][1:])
        
        return base_currency_id, target_currency_id, amount
        
    def handle_convert(self, path: str) -> dict:
        base_currency_id, target_currency_id, amount = \
            Service.parse_coords(path)
        
        logger.info(
            f"Entered in handle_convert function with path: {path}, "
            f"base_currency_code: {base_currency_id}, "
            f"target_currency_code: {target_currency_id} "
            f"and amount: {amount}"
            )
        
        exchange_rates = ConvertValueDTO(
            base_currency_id,
            target_currency_id, amount=amount
            )
        
        if self.exchange_rates.read_row(exchange_rates) != []:
            exchange_rates.rate = self.__get_rate(exchange_rates) 
            exchange_rates.converted_amount = exchange_rates.rate * amount
            
            logger.info(
            f"{base_currency_id} - {target_currency_id} rate exists and = "
            f"{exchange_rates.rate} with amount = "
            f"{exchange_rates.converted_amount}"
            )
             
            return exchange_rates.to_dict()
        
        exchange_rates.target_currency_id, exchange_rates.base_currency_id = \
            exchange_rates.base_currency_id, exchange_rates.target_currency_id
        
        if self.exchange_rates.read_row(exchange_rates) != []:    
            exchange_rates.rate = 1 / self.__get_rate(exchange_rates) 
            exchange_rates.converted_amount = exchange_rates.rate * amount
            
            logger.info(
            f"{target_currency_id} - {base_currency_id} rate exists and = "
            f"{exchange_rates.rate} with amount = "
            f"{exchange_rates.converted_amount}"
            )
            
            return exchange_rates.to_dict()
        
        exchange_rates.target_currency_id, exchange_rates.base_currency_id = \
            exchange_rates.target_currency_id, exchange_rates.base_currency_id
            
        exchange_rates_a = ConvertValueDTO("USD", base_currency_id, amount)
        exchange_rates_b = ConvertValueDTO("USD", target_currency_id, amount)
        
        if self.exchange_rates.read_row(exchange_rates_a) != [] and \
            self.exchange_rates.read_row(exchange_rates_b) != []:
                
            exchange_rates.rate = self.__get_rate(exchange_rates_b) \
                / self.__get_rate(exchange_rates_a)
                
            exchange_rates.converted_amount = \
                exchange_rates.rate * exchange_rates.amount
            
            logger.info(
            f"{target_currency_id} - {base_currency_id} rate exists and = "
            f"{exchange_rates.rate} with amount = "
            f"{exchange_rates.converted_amount}"
            )
            
            return exchange_rates.to_dict()