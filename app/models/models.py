import sqlite3
from random import randint\

from services.functions import read
from static.consts import PATHS

class WordsTable():
    def __init__(self):
        self.connection = sqlite3.connect(PATHS.get('database'))
        self.cursor = self.connection.cursor()
        
    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Words (
        id INTEGER PRIMARY KEY,
        word TEXT NOT NULL
        )
        ''')
        self.fill_table()
    
    def fill_table(self):
        self.data = read(PATHS["words"])
        number = randint(1, len(self.data))
        self.cursor.execute(
            'INSERT INTO Words (id, word) VALUES (?, ?)',
            (f'{number}', f'{self.data[number]}')
            )
        self.connection.commit()

    def clear_table(self):
        self.cursor.execute('DELETE FROM "Words"')
        self.connection.commit()
        
    def get_word(self):
        self.cursor.execute('SELECT word FROM Words')
        word = self.cursor.fetchall()
        word = str(word[0])
        return word[2:-5]
        
    def __del__(self):
        self.connection.close()

