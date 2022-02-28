import sys
import validators
import urllib.request
from bullscows import gameplay, simple_ask, simple_inform

def get_dict(path):
    """
    Get dictionary from path.
    """
    if validators.url(path):
        with urllib.request.urlopen(path) as url:
            d = url.read().decode().splitlines()
    else:
        with open(path, 'r') as f:
            d = f.read().splitlines()
    return d


def main(dictionary_path:str, length:int=5):
    length = int(length)
    dictionary = get_dict(dictionary_path)
    dictionary = list(filter(lambda x:len(x)==length, dictionary))
    n_tries = gameplay(simple_ask, simple_inform, dictionary)
    print('Количество попыток:', n_tries)
    return

if __name__ == '__main__':
    main(*sys.argv[1:])
