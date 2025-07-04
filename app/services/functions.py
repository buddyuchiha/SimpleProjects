from static.consts import PATHS

def read(filepath: str):
    with open(filepath, 'r', encoding='UTF-8') as file:
        data = file.readlines()
        return data
    
def helper(word, hide_word, desicion):
    for i in range(len(word)):
        if desicion == word[i]:
            hide_word[i] = desicion
    return hide_word
    
