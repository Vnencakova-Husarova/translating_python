

class AtomicComparison:

    def __init__(self, first, second, operator):
        self._first = first
        self._second = second
        self._operator = operator

    def toString(self):
        string = self._first + " " + self._operator + " " + self._second
        return string