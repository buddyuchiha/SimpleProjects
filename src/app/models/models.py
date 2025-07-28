from app.models.connect_manager import Connection
from app.models.currencies_migration import cur_mirgation
from app.models.exchange_rates_migration import ex_migration
from app.utils.logging import logger
from app.utils.dto import CurrencyDTO, ExchangeRatesDTO, ConvertValueDTO
from core.config import config

class Currencies:
    def __init__(self) -> None:
        cur_mirgation(config['DATABASE']['PATH'])
        
    def create(self, currency: CurrencyDTO) -> None:
        with Connection(config['DATABASE']['PATH']) as db:
            db.cur.execute(
                """
                INSERT INTO currencies (code, full_name, sign)
                VALUES (?, ?, ?);           
                """,
                (currency.code, currency.full_name, currency.sign)
            )
            db.conn.commit()
        
            logger.info("Creating record to the Currencies table")

    def read(self) -> list:
        with Connection(config['DATABASE']['PATH']) as db:
            db.cur.execute(
                """
                SELECT *
                FROM currencies
                """
            )
        
            logger.info("Reading data from the Currencies table")
            
            rows = db.cur.fetchall()
            return [CurrencyDTO(row[0], row[1], row[2], row[3]).to_dict() for row in rows]
    
    def read_row(self, code: str) -> list:
        with Connection(config['DATABASE']['PATH']) as db:
            db.cur.execute(
                """
                SELECT *
                FROM currencies
                WHERE code = ?
                """,
                (code, )
            )
            
            logger.info("Reading data from the Currencies table")
            
            rows = db.cur.fetchall()
            return [CurrencyDTO(row[0], row[1], row[2], row[3]).to_dict() for row in rows]

    def update(self, column: str, id: int, value: any) -> None:
        allowed_columns = ["code", "full_name", "sign"]
        if column not in allowed_columns:
            raise ValueError(f"Недопустимое имя столбца: {column}")
        with Connection(config['DATABASE']['PATH']) as db:
            db.cur.execute(
                f"""
                UPDATE currencies 
                SET {column} = ?
                WHERE id = ? 
                """,
                (value, id)
            )
            db.conn.commit()
            
            logger.info(
                f"Updated record for column: {column}, "
                f"value: {value} and id: {id} at the Currencies table")
    
    def delete(self, id: int) -> None:
        with Connection(config['DATABASE']['PATH']) as db:
            db.cur.execute(
                """
                DELETE FROM currencies
                WHERE id = ?
                """,
                (id, )
            )
            db.conn.commit()
            
            logger.info(f"Deleted record for id: {id} at the Currencies table")
            
                      
class ExchangeRates:
    def __init__(self):
        ex_migration(config['DATABASE']['PATH'])

    def create(self, exchange_rate: ExchangeRatesDTO) -> None:
        with Connection(config['DATABASE']['PATH']) as db:
            db.cur.execute(
                """
                INSERT INTO exchange_rates (
                    base_currency_id, target_currency_id, rate
                    )
                VALUES (?, ?, ?)
                """, 
                (exchange_rate.base_currency_id, exchange_rate.target_currency_id, exchange_rate.rate)
            )
            db.conn.commit()
            
            logger.info("Creating record to the ExchangeRates table")
        
    def read(self) -> list:
        with Connection(config['DATABASE']['PATH']) as db:
            db.cur.execute(
            """
                SELECT 
                    exchange_rates.id,
                    json_object(
                        'id', base_currencies.id,
                        'name', base_currencies.code,
                        'code', base_currencies.full_name,
                        'sign', base_currencies.sign
                    ) AS "base_currency",
                    json_object(
                        'id', target_currencies.id,
                        'name', target_currencies.code,
                        'code', target_currencies.full_name,
                        'sign', target_currencies.sign
                    ) AS "target_currency",
                    exchange_rates.rate
                FROM exchange_rates
                JOIN currencies base_currencies
                ON exchange_rates.base_currency_id = base_currencies.id
                JOIN currencies target_currencies
                ON exchange_rates.target_currency_id = target_currencies.id
                """
            )
            
            logger.info("Reading data from the ExchangeRates table")
            
            rows = db.cur.fetchall()
            
            return [ExchangeRatesDTO(row[0], row[1], row[2], row[3]).to_dict() for row in rows]

    def read_row(self, exchange_rate: ExchangeRatesDTO | ConvertValueDTO):
        with Connection(config['DATABASE']['PATH']) as db:
            db.cur.execute(
                """
                    SELECT 
                        exchange_rates.id,
                        json_object(
                            'id', base_currencies.id,
                            'name', base_currencies.code,
                            'code', base_currencies.full_name,
                            'sign', base_currencies.sign
                        ) AS "base_currency",
                        json_object(
                            'id', target_currencies.id,
                            'name', target_currencies.code,
                            'code', target_currencies.full_name,
                            'sign', target_currencies.sign
                        ) AS "target_currency",
                        exchange_rates.rate
                    FROM exchange_rates
                    JOIN currencies base_currencies
                    ON exchange_rates.base_currency_id = base_currencies.id
                    JOIN currencies target_currencies
                    ON exchange_rates.target_currency_id = target_currencies.id
                    WHERE base_currencies.code = ? and target_currencies.code = ?
                    """,
                    (exchange_rate.base_currency_id, exchange_rate.target_currency_id)
                )
            
            logger.info("Reading data from the ExchangeRates table")
            
            rows = db.cur.fetchall()
            
            return [ExchangeRatesDTO(row[0], row[1], row[2], row[3]).to_dict() for row in rows]

    def update(self, exchange_rate: ExchangeRatesDTO) -> None:
        with Connection(config['DATABASE']['PATH']) as db:
            db.cur.execute(
                f"""
                UPDATE exchange_rates
                SET rate = ?
                WHERE base_currency_id = (SELECT id FROM currencies WHERE code = ?) and target_currency_id = (SELECT id FROM currencies WHERE code = ?)
                """,
                (exchange_rate.rate, exchange_rate.base_currency_id, exchange_rate.target_currency_id)
            )
            db.conn.commit()
        
            logger.info(
                f"Updated record for base_id: {exchange_rate.base_currency_id} and target_id: {exchange_rate.target_currency_id}, "
                f"value: {exchange_rate.rate} at the ExchangeRates table")
    
    def delete(self, id: int) -> None:
        with Connection(config['DATABASE']['PATH']) as db:
            db.cur.execute(
                """
                DELETE FROM exchange_rates
                WHERE id = ?
                """,
                (id, )
            )
            db.conn.commit()
            
            logger.info(f"Deleted record for id: {id} at the ExchangeRates table")