from abc import ABC, abstractmethod
import sqlite3 as sq

from core import config
from app.services.logging import logger


class Currencies:
    def __init__(self) -> None:
        self.con = sq.connect(config.CURRENCIES_DB_PATH)
        self.con.row_factory = sq.Row 
         
        self.cur = self.con.cursor()
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS currencies (
                id INTEGER PRIMARY KEY,
                code TEXT UNIQUE,
                full_name TEXT,
                sign TEXT
            );
            """
        )
        
        logger.info("(Re-)Created Currencies table")
       
    def create(self, full_name: str, code: str, sign: str) -> None:
        self.cur.execute(
            """
            INSERT INTO currencies (code, full_name, sign)
            VALUES (?, ?, ?);           
            """,
            (code, full_name, sign)
        )
        self.con.commit()
        
        logger.info("Creating record to the Currencies table")

    def read(self) -> list:
        self.cur.execute(
            """
            SELECT *
            FROM currencies
            """
        )
        
        logger.info("Reading data from the Currencies table")
        
        rows = self.cur.fetchall()
        return [dict(row) for row in rows]
    
    def read_row(self, code: str) -> list:
        self.cur.execute(
            """
            SELECT *
            FROM currencies
            WHERE code = ?
            """,
            (code, )
        )
        
        logger.info("Reading data from the Currencies table")
        
        rows = self.cur.fetchall()
        return [dict(row) for row in rows]

    def update(self, column: str, id: int, value: any) -> None:
        allowed_columns = ["code", "full_name", "sign"]
        if column not in allowed_columns:
            raise ValueError(f"Недопустимое имя столбца: {column}")
        
        self.cur.execute(
            f"""
            UPDATE currencies 
            SET {column} = ?
            WHERE id = ? 
            """,
            (value, id)
        )
        self.con.commit()
        
        logger.info(
            f"Updated record for column: {column}, "
            f"value: {value} and id: {id} at the Currencies table")
    
    def delete(self, id: int) -> None:
        self.cur.execute(
            """
            DELETE FROM currencies
            WHERE id = ?
            """,
            (id, )
        )
        self.con.commit()
        
        logger.info(f"Deleted record for id: {id} at the Currencies table")
        
    def __del__(self):
        self.con.close()
        logger.info("Currencies table closed")
        
              
class ExchangeRates:
    def __init__(self):
        self.con = sq.connect(config.EXCHANGE_RATES_DB_PATH)
        self.con.row_factory = sq.Row
        
        self.cur = self.con.cursor()
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY,
                base_currency_id INTEGER UNIQUE,
                target_currency_id INTEGER UNIQUE,
                rate DECIMAL(6)
            );
            """            
        )
        
        logger.info("(Re-)Created ExchangeRates table") 

    def create(
        self, 
        base_currency_id: str, 
        target_currency_id: str, 
        rate: float
        ) -> None:
        self.cur.execute(
            """
            INSERT INTO exchange_rates (
                base_currency_id, target_currency_id, rate
                )
            VALUES (?, ?, ?)
            """, 
            (base_currency_id, target_currency_id, rate)
        )
        self.con.commit()
        
        logger.info("Creating record to the ExchangeRates table")
        
    def read(self) -> list:
        self.cur.execute(
            """
            SELECT *
            FROM exchange_rates
            """
        )
        
        logger.info("Reading data from the ExchangeRates table")
        
        rows = self.cur.fetchall()
        return [dict[row] for row in rows]

    def update(self, column: str, id: int, value: str) -> None:
        allowed_columns = ["base_currency_id", "target_currency_id", "rate"]
        if column not in allowed_columns:
            raise ValueError(f"Недопустимое имя столбца: {column}")
        
        self.cur.execute(
            f"""
            UPDATE exchange_rates
            SET {column} = ?
            WHERE id = ? 
            """,
            (value, id)
        )
        self.con.commit()
        
        logger.info(
            f"Updated record for column: {column}, "
            f"value: {value} and id: {id} at the ExchangeRates table")
    
    def delete(self, id: int) -> None:
        self.cur.execute(
            """
            DELETE FROM exchange_rates
            WHERE id = ?
            """,
            (id, )
        )
        self.con.commit()
        
        logger.info(f"Deleted record for id: {id} at the ExchangeRates table")
            
    def __del__(self):
        self.con.close()
        logger.info("ExchangeRates table closed")