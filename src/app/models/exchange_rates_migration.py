from app.models.connect_manager import Connection
from app.utils.logging import logger


def ex_migration(path: str):
    with Connection(path) as db:
        db.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY,
                base_currency_id INTEGER,
                target_currency_id INTEGER,
                rate DECIMAL(6),
                FOREIGN KEY(base_currency_id) REFERENCES currencies(id),
                FOREIGN KEY(target_currency_id) REFERENCES сurrencies(id),
                UNIQUE(base_currency_id, target_currency_id)
            );
            """    
        )
        
        logger.info("(Re-)Created ExchangeRates table")
 
        
def ex_migration_2(path: str):
    with Connection(path) as db:
        db.cur.execute(
            """
            DROP DATABASE IF EXISTS exchange_rates
            )
            """
        )
        
        logger.info("Deleted Exchange Rates table")
        