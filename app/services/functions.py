def read(filepath: str, key_word: str):
    with open(filepath, 'r', encoding='UTF-8') as file:
        data = file.read()
        return data
    
