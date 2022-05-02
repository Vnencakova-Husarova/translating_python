from AtomicComparison import AtomicComparison
from Predicate import Predicate
import inspect


class Parser:
    i = 0
    _chars_predicate = '-_qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM'
    _chars_atribute = 'QWERTZUIOPASDFGHJKLYXCVBNM'

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

    def read_name(self, char_set):
        self.spaces()
        name = ''
        while self.i < len(self._string) and \
                self._string[self.i] in char_set:
            name += self._string[self.i]
            self.i += 1

        return name

    def read_int(self):
        self.spaces()
        integer = ''

        while self.i < len(self._string) and \
                self._string[self.i] in '0123456789':
            integer += self._string[self.i]
            self.i += 1

        return integer

    def read_predicate(self, neg, new_p):
        self.spaces()
        name = self.read_name(self._chars_predicate)
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
                if self._string[self.i] != ',':
                    return None
                self.i += 1
                self.spaces()

            if self._string[self.i] == '\'':
                self.i += 1
                con = ''
                while self.i < len(self._string) and self._string[self.i] != '\'':
                    con += self._string[self.i]
                    self.i += 1
                self.i += 1
                result.add_atribute(con)

            elif self._string[self.i] == '_' and not new_p:
                result.add_atribute('_')
                self.i += 1

            elif self._string[self.i] < 'A' or self._string[self.i] > 'Z' or self._string[self.i] == '_':
                return None

            else:
                result.add_atribute(self.read_name(self._chars_atribute))

            self.spaces()
            tmp = True
        self.i += 1
        self.spaces()
        return result

    def read_condition(self, neg):
        first = self.read_name(self._chars_atribute)

        if first is None:
            return None

        self.spaces()
        operator = ''
        ## = < > <= >=

        if self._string[self.i] == '=':
            operator = '='
            self.i += 1
        elif self._string[self.i] == '<':
            self.i += 1
            if self._string[self.i] == '=':
                operator = '<='
                self.i += 1
            else:
                operator = '<'
        elif self._string[self.i] == '>':
            self.i += 1
            if self._string[self.i] == '=':
                operator = '>='
                self.i += 1
            else:
                operator = '>'
        else:
            return Exception('CONDITION ZLY OPERATOR')

        self.spaces()
        second = ''
        is_int = False
        if '0' <= self._string[self.i] <= '9':
            second = self.read_int()
            is_int = True
        elif 'A' <= self._string[self.i] <= 'Z':
            second = self.read_name(self._chars_atribute)

        if second is None:
            return None

        comparison = AtomicComparison(first, second, operator)
        if neg:
            comparison.negate()
        if is_int:
            comparison.second_int()

        return comparison

    def read_next(self):
        tmp = self.negation()
        self.spaces()
        if isinstance(tmp, Exception):
            return Exception('negacia')

        if 'a' <= self._string[self.i] <= 'z':
            return self.read_predicate(tmp, False)

        if 'A' <= self._string[self.i] <= 'Z':
            return self.read_condition(tmp)

    def parse_line(self):
        self.spaces()
        predicate = self.read_predicate(False, True)
        self.spaces()

        if predicate is None:
            return None

        if self._string[self.i] == ':':
            self.i += 1
            self.spaces()

            if self._string[self.i] == '-':
                self.i += 1
                self.spaces()
            else:
                return None

        tmp = False
        while self.i < len(self._string) and self._string[self.i] != '.':
            self.spaces()
            if tmp:
                if self._string[self.i] != ',':
                    return None
                self.i += 1
                self.spaces()

            next = self.read_next()

            if next is None:
                return None

            if isinstance(next, Predicate):
                predicate.add_atomic_predicate(next)
            else:
                predicate.add_comparison(next)
            tmp = True

        if self.i == len(self._string):
            return None
        self.i += 1

        return predicate

    def parse(self):
        predicates = []
        while self.i < len(self._string):
            tmp = self.parse_line()
            self.spaces()
            if tmp is None:
                return None
            #        if self._string[self.i] < 'a' or self._string[self.i] > 'z': return None
            predicates.append(tmp)
        return predicates
