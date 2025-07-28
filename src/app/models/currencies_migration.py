from app.models.connect_manager import Connection
from app.utils.logging import logger


def cur_mirgation(path: str):
    with Connection(path) as db:
        db.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS currencies (
                id INTEGER PRIMARY KEY,
                code TEXT UNIQUE,
                full_name TEXT,
                sign TEXT
            )
            """
        )
        
        logger.info("(Re-)Created Currencies table")
        

def cur_migration_2(path: str):
    with Connection(path) as db:
        db.cur.execute(
            """
            DROP DATABASE IF EXISTS currencies
            )
            """
        )
        
        logger.info("Deleted Currencies table")