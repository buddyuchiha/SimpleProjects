from dataclasses import dataclass
from typing import Optional, Class

@dataclass(frozen=True)
class CurrencyDTO:
    id: Optional[int] = None
    code: str 
    full_name: str 
    sign: str
    
    def __post_init__(self) -> None:
        if not isinstance(self.code, str) or not isinstance(self.full_name, str) or not isinstance(self.sign, str):
            raise TypeError("Wrong type")
        
    def to_dict(self) -> dict:
        return {
            "id"        : self.id,
            "code"      : self.code,
            "full_name" : self.full_name,
            "sign"      : self.sign
        }
        
    @classmethod    
    def from_dict(cls, data: dict) -> Class:
        return cls(
            id = data["id"],
            code = data["code"],
            full_name = data["full_name"],
            sign = data["sign"]
        )