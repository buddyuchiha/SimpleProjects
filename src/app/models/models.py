import sqlite3 as sq

from core import config
from app.services.logging import logger


class Currencies:
    
    def __init__(self):
        with sq.connect(config.CURRENCIES_DB_PATH) as con:
            cur = con.cursor()
            
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS currencies (
                    id INTEGER PRIMARY KEY,
                    code TEXT,
                    full_name TEXT UNIQUE,
                    sign TEXT
                );
                """
            )
        logger.info("(Re-)Created Currencies table")      


class ExchangeRates:
    
    def __init__(self):
        with sq.connect(config.EXCHANGE_RATES_DB_PATH) as con:
            cur = con.cursor()
            
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS exchange_rates (
                    id INTEGER PRIMARY KEY,
                    base_currency_id INTEGER UNIQUE,
                    target_currency_id INTEGER UNIQUE,
                    rate DECIMAL(6)
                )
                """            
            )
        logger.info("(Re-)Created ExchangeRates table")   