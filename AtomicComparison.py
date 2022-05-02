class AtomicComparison:

    def __init__(self, first, second, operator):
        self._neg = False
        self._sec_int = False
        self._first = first
        self._second = second
        self._operator = operator

    def toString(self):
        string = self._first + " " + self._operator + " " + self._second
        return string

    def negate(self):
        self._neg = True

    def second_int(self):
        self._sec_int = True

    def is_second_int(self):
        return self._sec_int
