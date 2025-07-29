from dataclasses import dataclass
import json

@dataclass
class CurrencyDTO:
    id        : int
    code      : str 
    full_name : str 
    sign      : str
        
    def to_dict(self) -> dict:
        return {
            "id"        : self.id,
            "code"      : self.code,
            "full_name" : self.full_name,
            "sign"      : self.sign
        }
        
@dataclass
class ExchangeRatesDTO:
    id                 : int
    base_currency_id   : dict
    target_currency_id : dict 
    rate               : float
    
    def to_dict(self) -> dict:
        return {
            "id"                 : self.id,
            "base_currency_id"   : json.loads(self.base_currency_id),
            "target_currency_id" : json.loads(self.target_currency_id),
            "rate"               : self.rate
        }
          
@dataclass
class ConvertValueDTO:
    base_currency_id     : str 
    target_currency_id   : str 
    rate                 : float = None
    amount               : int = None
    converted_amount     : int = None
    
    def to_dict(self) -> dict:
        return {
            "base_currency_id"     : self.base_currency_id, 
            "target_currency_id"   : self.target_currency_id,
            "rate"                 : self.rate,
            "amount"               : self.amount,
            "converted_amount"     : self.converted_amount
        }