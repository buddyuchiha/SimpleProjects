def read(filepath: str) -> list[str]:
    with open(filepath, 'r', encoding='UTF-8') as file:
        data = file.readlines()
        return data
  
    
def helper(word: str, hide_word: str, desicion: str) -> list[str]:
    for i in range(len(word)):
        if desicion == word[i]:
            hide_word[i] = desicion
    return hide_word