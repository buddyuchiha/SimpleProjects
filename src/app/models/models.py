import json

from core import config
from app.models.connect_manager import Connection
from app.models.currencies_migration import cur_mirgation
from app.models.exchange_rates_migration import ex_migration
from app.utils.logging import logger


class Currencies:
    def __init__(self) -> None:
        cur_mirgation(config.DB_PATH)
        
    def create(self, full_name: str, code: str, sign: str) -> None:
        with Connection(config.DB_PATH) as db:
            db.cur.execute(
                """
                INSERT INTO currencies (code, full_name, sign)
                VALUES (?, ?, ?);           
                """,
                (code, full_name, sign)
            )
            db.conn.commit()
        
            logger.info("Creating record to the Currencies table")

    def read(self) -> list:
        with Connection(config.DB_PATH) as db:
            db.cur.execute(
                """
                SELECT *
                FROM currencies
                """
            )
        
            logger.info("Reading data from the Currencies table")
            
            rows = db.cur.fetchall()
            return [dict(row) for row in rows]
    
    def read_row(self, code: str) -> list:
        with Connection(config.DB_PATH) as db:
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
            return [dict(row) for row in rows]

    def update(self, column: str, id: int, value: any) -> None:
        allowed_columns = ["code", "full_name", "sign"]
        if column not in allowed_columns:
            raise ValueError(f"Недопустимое имя столбца: {column}")
        with Connection(config.DB_PATH) as db:
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
        with Connection(config.DB_PATH) as db:
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
        ex_migration(config.DB_PATH)

    def create(
        self, 
        base_currency_id: str, 
        target_currency_id: str, 
        rate: float
        ) -> None:
        with Connection(config.DB_PATH) as db:
            db.cur.execute(
                """
                INSERT INTO exchange_rates (
                    base_currency_id, target_currency_id, rate
                    )
                VALUES (?, ?, ?)
                """, 
                (base_currency_id, target_currency_id, rate)
            )
            db.conn.commit()
            
            logger.info("Creating record to the ExchangeRates table")
    
    @staticmethod        
    def handle_answer(rows: list[tuple]) -> dict:
        result = []
        
        for row in rows:
            row_dict = dict(row)
            row_dict["base_currency"] = json.loads(row_dict["base_currency"])
            row_dict["target_currency"] = json.loads(row_dict["target_currency"])
            result.append(row_dict)
        
        return result   
        
    def read(self) -> list:
        with Connection(config.DB_PATH) as db:
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
            result = ExchangeRates.handle_answer(rows)
            
            return rows

    def read_row(self, first_code: str, second_code: str):
        with Connection(config.DB_PATH) as db:
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
                    (first_code, second_code)
                )
            
            logger.info("Reading data from the ExchangeRates table")
            
            rows = db.cur.fetchall()
            result = ExchangeRates.handle_answer(rows)
            
            return result

    def update(self, base_id: int, target_id: int, value: int) -> None:
        with Connection(config.DB_PATH) as db:
            db.cur.execute(
                f"""
                UPDATE exchange_rates
                SET rate = ?
                WHERE base_currency_id = (SELECT id FROM currencies WHERE code = ?) and target_currency_id = (SELECT id FROM currencies WHERE code = ?)
                """,
                (value, base_id, target_id)
            )
            db.conn.commit()
        
            logger.info(
                f"Updated record for base_id: {base_id} and target_id: {target_id}, "
                f"value: {value} at the ExchangeRates table")
    
    def delete(self, id: int) -> None:
        with Connection(config.DB_PATH) as db:
            db.cur.execute(
                """
                DELETE FROM exchange_rates
                WHERE id = ?
                """,
                (id, )
            )
            db.conn.commit()
            
            logger.info(f"Deleted record for id: {id} at the ExchangeRates table")