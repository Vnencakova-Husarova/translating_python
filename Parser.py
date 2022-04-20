class Parser:
    i = 0
    _string = ''
    WRONG = -4

    def __init__(self, string):
        self._string = string
        self._charsPredicate = '-_qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM'
        self._charsAtribute = 'QWERTZUIOPASDFGHJKLYXCVBNM'

    def spaces(self):
        while self.i < self._string.length() and self._string[self.i] == ' ':
            self.i += 1

    def negation(self):
        if self._string[self.i] == '\\':
            self.i += 1
            if self._string[self.i] == '+':
                self.i += 1
                self.spaces()
                return True
            else:
                return self.WRONG
        else:
            return False

    def readName(self, charSet):
        name = ''
        while self.i < self._string.length() and \
                self._string[self.i] in charSet:
            name += self._string[self.i]
            self.i += 1

        return name

    def readPredicate(self, neg, newP):
        name = self.readName(self._charsPredicate)
        self.spaces()

        if self._string[self.i] != '(':
            return None
        self.i += 1

        from Predicate import Predicate
        result = Predicate(name)

        if neg:
            result.negate()

        self.spaces()
        tmp = False

        while self.i < self._string.length() and self._string[self.i] != ')':
            if tmp:
                if self._string[self.i] != ',': return None
                self.i += 1
                self.spaces()

            if self._string[self.i] == '\'':
                self.i += 1
                con = ''
                while self.i < self._string.length() and self._string[self.i] != '\'':
                    con += self._string[self.i]
                    self.i += 1
                self.i += 1
                result.addAtribute(con)

            elif self._string[self.i] == '_' and not newP:
                result.addAtribute('_')
                self.i += 1

            elif self._string[self.i] < 65 or self._string[self.i] > 90 or self._string[self.i] == '_':
                return None

            else:
                result.addAtribute(self.readName(self._charsAtribute))

            self.spaces()
            tmp = True

        return result


    def readNext(self):
        tmp = self.negation()

        if tmp == self.WRONG: return self.WRONG

        if 97 <= self._string[self.i] <= 122:
            self.readPredicate(tmp, False)

        if 65 <= self._string[self.i] <= 90:
            self.readCondition(tmp)
