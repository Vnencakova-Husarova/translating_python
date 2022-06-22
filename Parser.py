from AtomicComparison import AtomicComparison
from Predicate import Predicate
import inspect


class Parser:
    i = 0
    _chars_predicate = '-_qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM'
    _chars_atribute = 'QWERTZUIOPASDFGHJKLYXCVBNM'

    def __init__(self, string):
        self._string = string
        self._problem = 'OK'

    def _spaces(self):
        while self.i < len(self._string) and self._string[self.i] == ' ':
            self.i += 1

    def _negation(self):
        if self._string[self.i] == '\\':
            self.i += 1
            self._spaces()
            if self._string[self.i] == '+':
                self.i += 1
                self._spaces()
                return True
            else:
                self._problem = 'NESPRAVNY ZAPIS NEGACIE'
                return True
        else:
            return False

    def _read_name(self, char_set):
        self._spaces()
        name = ''
        while self.i < len(self._string) and \
                self._string[self.i] in char_set:
            name += self._string[self.i]
            self.i += 1

        if name == '':
            self._problem = 'NESPRÁVNY FORMÁT ZÁPISU - meno'
            return None

        return name

    def _read_int(self):
        self._spaces()
        integer = ''

        while self.i < len(self._string) and \
                self._string[self.i] in '0123456789':
            integer += self._string[self.i]
            self.i += 1

        if integer == '':
            self._problem = 'NESPRÁVNY FORMÁT ZÁPISU - číslo'
            return None

        return integer

    def read_predicate(self, neg, new_p):
        self._spaces()
        name = self._read_name(self._chars_predicate)
        self._spaces()

        if self._string[self.i] != '(':
            self._problem = 'NESPRÁVNY FORMÁT ZÁPISU - chýba zátvorka'
            return None
        self.i += 1

        from Predicate import Predicate
        result = Predicate(name)

        if neg:
            result.negate()

        self._spaces()
        tmp = False

        while self.i < len(self._string) and self._string[self.i] != ')':
            if tmp:
                if self._string[self.i] != ',':
                    self._problem = 'NESPRÁVNY FORMÁT ZÁPISU - chýba čiarka'
                    return None
                self.i += 1
                self._spaces()

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
                self._problem = 'NESPRÁVNY FORMÁT ZÁPISU - zlý atribút v predikáte'
                return None

            else:
                result.add_atribute(self._read_name(self._chars_atribute))

            self._spaces()
            tmp = True
        self.i += 1
        self._spaces()
        return result

    def _read_condition(self, neg):
        first = self._read_name(self._chars_atribute)

        if first is None:
            return None

        self._spaces()
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
            self._problem = 'CONDITION ZLÝ OPERATOR'
            return None

        self._spaces()
        second = ''
        is_int = False
        if '0' <= self._string[self.i] <= '9':
            second = self._read_int()
            is_int = True
        elif 'A' <= self._string[self.i] <= 'Z':
            second = self._read_name(self._chars_atribute)

        if second is None:
            return None

        comparison = AtomicComparison(first, second, operator)
        if neg:
            comparison.negate()
        if is_int:
            comparison.second_int()

        return comparison

    def _read_next(self):
        tmp = self._negation()
        self._spaces()
        if tmp and not self._problem == 'OK':
            return None

        if 'a' <= self._string[self.i] <= 'z':
            return self.read_predicate(tmp, False)

        if 'A' <= self._string[self.i] <= 'Z':
            return self._read_condition(tmp)

        else:
            self._problem = 'ZLÝ FORMÁT ZÁPISU'
            return None

    def _parse_line(self):
        self._spaces()
        predicate = self.read_predicate(False, True)
        self._spaces()

        if predicate is None:
            return None

        if self._string[self.i] == ':':
            self.i += 1
            self._spaces()

            if self._string[self.i] == '-':
                self.i += 1
                self._spaces()
            else:
                self._problem = 'NESPRÁVNY FORMÁT ZÁPISU'
                return None

        tmp = False
        while self.i < len(self._string) and self._string[self.i] != '.':
            self._spaces()
            if tmp:
                if self._string[self.i] != ',':
                    self._problem = 'NESPRÁVNY FORMÁT ZÁPISU - chýba čiarka'
                    return None
                self.i += 1
                self._spaces()

            next = self._read_next()

            if next is None:
                return None

            if isinstance(next, Predicate):
                predicate.add_atomic_predicate(next)
            else:
                predicate.add_comparison(next)
            tmp = True

        if self.i == len(self._string):
            self._problem = 'NESPRÁVNY FORMÁT ZÁPISU - chýba bodka'
            return None
        self.i += 1

        return predicate

    def parse(self):
        predicates = []
        while self.i < len(self._string):
            tmp = self._parse_line()
            self._spaces()
            if tmp is None:
                return None
            #        if self._string[self.i] < 'a' or self._string[self.i] > 'z': return None
            predicates.append(tmp)
        return predicates

    def get_problem(self):
        return self._problem
