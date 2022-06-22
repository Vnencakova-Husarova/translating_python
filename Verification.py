class Verification:
    _tables_set = set()
    _tables_original = set()

    def __init__(self, tables):
        self._predicate = []
        self._tables_original.update(tables)
        self._tables_set.update(tables)
        self._problem = 'OK'

    def set_predicate(self, predicate):
        self._predicate = predicate

    def check_neg(self):
        if self._predicate._neg and self._predicate.contains_atribute('_'):
            self._problem = 'NEGOVANÝ PREDIKÁT OBSAHUJE VOĽNÚ PREMENNÚ'
            return False
        return True

    def check_not_recursive(self):
        tmp = self._predicate._atomic_predicates
        for p in tmp:
            if p._name == self._predicate._name:
                self._problem = 'REKURZIA'
                return False

        return True

    def check_safety(self):
        positive_atributes_set = set()  # overujem ci negativne boli najskor spomenute v pozitivnom vyzname
        number_occurence = {}  # overujem ci boli atributy spomenute aspon raz aj v druhej casti

        if self._predicate._name in self._tables_original:
            self._problem = 'PREDEFINOVANIE HOTOVÉHO PREDIKÁTU'
            return False

        for a in self._predicate._atributes:
            number_occurence[a] = 0

        tmp_verification = Verification(self._tables_set)

        if not self.check_not_recursive():
            return False

        for p in self._predicate._atomic_predicates:

            if not p.check_neg(tmp_verification):
                self._problem = 'NEGOVANÝ PREDIKÁT OBSAHUJE VOĽNÚ PREMENNÚ'
                return False

            if not p._name in self._tables_set:
                self._problem = 'POUŽITÝ NEZNÁMY PREDIKÁT'
                return False

            for a in p._atributes:
                if a in number_occurence:
                    number_occurence[a] += 1
                else:
                    number_occurence[a] = 0

                if not p._neg:
                    positive_atributes_set.add(a)
                else:
                    if not a in positive_atributes_set:
                        self._problem = 'ATRIBÚT NEBOL NAJSKÔR V POZITÍVNOM KONTEXTE'
                        return False

        for a in self._predicate._atributes:
            if number_occurence[a] == 0:
                self._problem = 'NESPOMENUTÝ ATRIBÚT'
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
                self._problem = 'PREMENNÁ IBA RAZ'
                return False

        #overuje aj vzhladom na predosle
        self._tables_set.add(self._predicate._name)
        return True

    def get_problem(self):
        return self._problem