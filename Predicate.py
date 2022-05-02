class Predicate:

#name, atributes alebo atributes
    def __init__(self, name):
        self._name = name
        self._neg = False
        self._atomicPredicates = []
        self._atomicComparisons = []
        self._atributes = []

    def negate(self):
        self._neg = True

    def addAtribute(self, atribute):
        self._atributes.append(atribute)

    def addAtributes(self, atributes):
        self._atributes.extend(atributes)

    def addAtomicPredicate(self, predicate):
        self._atomicPredicates.append(predicate)

    def addComparison(self, comparison):
        self._atomicComparisons.append(comparison)

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

