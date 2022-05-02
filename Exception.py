import string


class Exception:
    def __init__(self, string):
        self._string = string

    def print(self):
        print('CHYBA V: ' + string)