import textdistance as td
from random import randrange

def bullscows(guess:str, riddle:str)->(int,int):
    """
    Bulls: # of the same letters in the same places.
    Cows: # of the same letters in any places.
    """
    bulls = len(guess) - td.hamming(guess, riddle)     
    cows = int(td.overlap(guess, riddle) * len(guess))
    return bulls, cows

def gameplay(ask:callable, inform:callable, words:list[str])->int:
    
    #0 Choose a word.
    riddle = words[randrange(len(words))]
    n_tries = 0
    win = False
   
    while not win:
        #1 Ask a guess.
        guess = ask('Введите слово: ', words)
        bulls, cows = bullscows(guess, riddle)
        #2 Print result
        inform('Быки: {}, Коровы: {}', bulls, cows)
        if bulls == len(riddle):
            win = True
        n_tries += 1

    return n_tries    

def simple_ask(prompt: str, valid: list[str] = None) -> str:
    correct = False
    while not correct:
        guess = input(prompt)
        if valid is None or guess in valid:
            correct = True
    return guess

def simple_inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))
    return
