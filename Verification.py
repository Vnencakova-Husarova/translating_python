class Verification:
    _tables_set = set()  # set stringov

    def __init__(self, tables):
        self._predicate = []
        self._tables_set.update(tables)

    def set_predicate(self, predicate):
        self._predicate = predicate

    def check_neg(self):
        if self._predicate._neg and self._predicate.contains_atribute('_'):
            return False
        return True

    def check_not_recursive(self):
        tmp = self._predicate._atomic_predicates
        for p in tmp:
            if p._name == self._predicate._name:
                return False

        return True

    def check_safety(self):
        positive_atributes_set = set()  # overujem ci negativne boli najskor spomenute v pozitivnom vyzname
        number_occurence = {}  # overujem ci boli atributy spomenute aspon raz aj v druhej casti

        for a in self._predicate._atributes:
            number_occurence[a] = 0

        tmp_verification = Verification(self._tables_set)

        for p in self._predicate._atomic_predicates:
            if (not p.check_neg(tmp_verification)) or not (p._name in self._tables_set):
                return False;

            for a in p._atributes:
                if a in number_occurence:
                    number_occurence[a] += 1
                else:
                    number_occurence[a] = 0

                if not p._neg:
                    positive_atributes_set.add(a)
                else:
                    if not a in positive_atributes_set:
                        return False

        for a in self._predicate._atributes:
            if number_occurence[a] == 0:
                return False

        for c in self._predicate._atomic_comparisons:
            if c._first in number_occurence:
                number_occurence[c._first] += 1

            else:
                number_occurence[c._first] = 0

            if not c.is_second_int:
                if c._second in number_occurence:
                    number_occurence[c._second] += 1

                else:
                    number_occurence[c._second] = 0

        for a in number_occurence.values():
            if a == 0:
                return Exception('PREMENNA IBA RAZ')

        return True
        # doriesit overovanie conditions
