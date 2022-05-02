class Predicate:

#name, atributes alebo atributes
    def __init__(self, name):
        self._name = name
        self._neg = False
        self._atomic_predicates = []
        self._atomic_comparisons = []
        self._atributes = []

    def negate(self):
        self._neg = True

    def add_atribute(self, atribute):
        self._atributes.append(atribute)

    def add_atributes(self, atributes):
        self._atributes.extend(atributes)

    def add_atomic_predicate(self, predicate):
        self._atomic_predicates.append(predicate)

    def add_comparison(self, comparison):
        self._atomic_comparisons.append(comparison)

    def check_neg(self, verification):
        verification.set_predicate(self)
        return verification.check_neg()

    def check_whole(self, verification):
        verification.set_predicate(self)
        return verification.check_not_recursive() and verification.check_safety()

    def contains_atribute(self, atribute):
        return atribute in self._atributes

    def index_of(self, atribute):
        return self._atributes.index(atribute)

