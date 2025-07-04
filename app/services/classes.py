from static.consts import PHRASES, ALPHABET, HANGMAN
from models.models import WordsTable
from .functions import helper

class PlayerClass():
    def __init__(self):
        print (PHRASES.get('begin'))
        
        self.table = WordsTable()
        self.choice()
        
    def choice(self):
        self.status = input(f"{PHRASES.get('choice')} ") 
        
        match self.status:
            case "start":
                self.start() 
            case "quit":
                self.quit() 
            case "reset":
                self.reset() 
            case _:
                print(PHRASES.get("wrong"))
                self.chocie() 
            
    def start(self):
        self.table.clear_table()
        self.table.create_table()
        self.word = [a for a in self.table.get_word()] 
        self.hide_word = [' ' for i in range(len(self.word))]
        self.used = []
        self.attempts = 7
        
        print(
            PHRASES.get("beauty"),
            PHRASES.get('word'), 
            self.hide_word
            )
        
        self.game()
    
    def quit(self):
        print(
            PHRASES.get("beauty"),
            PHRASES.get('quit'),
            PHRASES.get("beauty")
            )
        
    def reset(self):
        self.table.clear_table()
        self.table.create_table()
        
        print(
            PHRASES.get("beauty"),
            PHRASES.get("reset"),
            PHRASES.get("beauty")
            )
        
        self.choice()
    
    def win(self):
        print(
            PHRASES.get("beauty"),
            PHRASES.get("win_lose"), 
            self.word,
            PHRASES.get("beauty")
            )
        
        self.choice()
    
    def lose(self):
        print(
            PHRASES.get("beauty"),
            PHRASES.get("end_lose"), 
            self.word, '\n',
            HANGMAN.get(self.attempts+1),
            PHRASES.get("beauty"),
            )
        
        self.choice()
        
    def game(self):
        while self.hide_word != self.word:
            if self.attempts <= 0:
                self.lose()
                break
            desicion = input(PHRASES.get('input')).lower()
            
            if desicion not in ALPHABET:
                print(PHRASES.get("rus"))
                self.game()
                
            if desicion in self.word:
                self.hide_word = helper(self.word, self.hide_word, desicion)
                self.used.append(desicion)
                
                print(
                    PHRASES.get('beauty'),
                    PHRASES.get('correct'), 
                    self.hide_word,
                    PHRASES.get("attempts"),
                    self.attempts,
                    PHRASES.get("used"),
                    self.used, '\n', 
                    HANGMAN.get(f"{self.attempts}"),
                    PHRASES.get('beauty')
                    )
            else:
                self.attempts -= 1
                self.used.append(desicion)
                
                print(
                    PHRASES.get('beauty'),
                    PHRASES.get('incorrect'), 
                    self.hide_word,
                    PHRASES.get("attempts"),
                    self.attempts,
                    PHRASES.get("used"),
                    self.used, '\n', 
                    HANGMAN.get(self.attempts+1),
                    PHRASES.get('beauty')
                    )
        self.win()
    