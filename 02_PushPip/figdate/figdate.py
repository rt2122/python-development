from pyfiglet import figlet_format 
from time import strftime

def date(fmt='%Y %d %b, %A', font='graceful'):
    return figlet_format(strftime(fmt), font=font) 
