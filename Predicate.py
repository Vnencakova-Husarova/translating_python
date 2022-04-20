class Predicate:
    _atomicPredicates = None
    _atomicComparisons = None
    _atributes = None

    def __init__(self, name, atributes):
        self._neg = False
        self._name = name
        self._atributes.extend(atributes)

    def __init__(self, name):
        self._name = name

    def negate(self):
        self._neg = True

    def addAtribute(self, atribute):
        self._atributes.extend(atribute)

    def addAtomicPredicate(self, predicate):
        self._atomicPredicates.extend(predicate)

    def addComparison(self, comparison):
        self._atomicComparisons.extend(comparison)

    def checkNeg(self, verification):
        verification.setPredicate(self)
        return verification.checkNeg()

    def checkWhole(self, verification):
        verification.setPredicate(self)
        return verification.checkNotRecursive() and verification.checkSafety()

    def containsAtribute(self, atribute):
        return atribute in self._atributes

    def indexOf(self, atribute):
        return self._atributes.index(atribute)

