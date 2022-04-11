class Verification:
    def __init__(self, tables):
        self._pedicate = None
        self._tablesSet.update(tables)

    def setPredicate(self, predicate):
        self._pedicate = predicate

    def checkNeg(self):
        if self._pedicate.getNeg(): return self._pedicate.containsAtribute('_')
        return True

    def checkNotRecursive(self):
        tmp = self._pedicate._predicates
        for p in tmp:
            if p._name == self._pedicate._name: return False

        return True

    def checkSafety(self):
        positiveAtributesSet = {}
        numberOccurenceMap = {}

        for a in self._pedicate._atributes:
            numberOccurenceMap[a] = 0

        