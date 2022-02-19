from figdate import date
from sys import argv
import locale

locale.setlocale(locale.LC_ALL, ('RU','UTF8'))
print(date(*argv[1:]))
