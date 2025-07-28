import sqlite3 as sq 

from app.utils.logging import logger

class Connection:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        
        logger.info("Database connected")
        
    def __enter__(self):
        self.conn = sq.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.cur.row_factory = sq.Row
        
        logger.info("Entered in connect manager")
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.close()
        
        logger.info("Connect manager closed")