from Predicate import Predicate
import inspect

class Parser:
    i = 0
    _charsPredicate = '-_qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM'
    _charsAtribute = 'QWERTZUIOPASDFGHJKLYXCVBNM'

    def __init__(self, string):
        self._string = string


    def spaces(self):
        while self.i < len(self._string) and self._string[self.i] == ' ':
            self.i += 1

    def negation(self):
        if self._string[self.i] == '\\':
            self.i += 1
            self.spaces()
            if self._string[self.i] == '+':
                self.i += 1
                self.spaces()
                return True
            else:
                return Exception('negacia')
        else:
            return False

    def readName(self, charSet):
        self.spaces()
        name = ''
        while self.i < len(self._string) and \
                self._string[self.i] in charSet:
            name += self._string[self.i]
            self.i += 1

        return name

    def readPredicate(self, neg, newP):
        self.spaces()
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

        while self.i < len(self._string) and self._string[self.i] != ')':
            if tmp:
                if self._string[self.i] != ',': return None
                self.i += 1
                self.spaces()

            if self._string[self.i] == '\'':
                self.i += 1
                con = ''
                while self.i < len(self._string) and self._string[self.i] != '\'':
                    con += self._string[self.i]
                    self.i += 1
                self.i += 1
                result.addAtribute(con)

            elif self._string[self.i] == '_' and not newP:
                result.addAtribute('_')
                self.i += 1

            elif self._string[self.i] < 'A' or self._string[self.i] > 'Z' or self._string[self.i] == '_':
                return None

            else:
                result.addAtribute(self.readName(self._charsAtribute))

            self.spaces()
            tmp = True
        self.i += 1
        self.spaces()
        return result

    #doriesit, domysliet
    def readCondition(self, neg):
        return None

    def readNext(self):
        tmp = self.negation()
        self.spaces()
        if isinstance(tmp, Exception): return Exception('negacia')

        if 'a' <= self._string[self.i] <= 'z':
            return self.readPredicate(tmp, False)

        if 'A' <= self._string[self.i] <= 'Z':
            return self.readCondition(tmp)



    def parseLine(self):
        self.spaces()
        predicate = self.readPredicate(False, True)
        self.spaces()

        if predicate is None: return None

        if self._string[self.i] == ':':
            self.i += 1
            self.spaces()

            if self._string[self.i] == '-':
                self.i += 1
                self.spaces()
            else: return None

        tmp = False
        while self.i < len(self._string) and self._string[self.i] != '.':
            self.spaces()
            if tmp:
                if self._string[self.i] != ',': return None
                self.i += 1
                self.spaces()

            next = self.readNext()

            if next is None: return None
            if isinstance(next, Predicate): predicate.addAtomicPredicate(next)
            else: predicate.addComparison(next)
            tmp = True

        if self.i == len(self._string) : return None
        self.i += 1

        return predicate

    def parse(self):
        predicates = []
        while self.i < len(self._string) :
            tmp = self.parseLine()
            self.spaces()
            if tmp == None: return None
    #        if self._string[self.i] < 'a' or self._string[self.i] > 'z': return None
            predicates.append(tmp)
        return predicates