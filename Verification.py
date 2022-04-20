class Verification:
    _tablesSet = None  # set stringov

    def __init__(self, tables):
        self._pedicate = None
        self._tablesSet.update(tables)

    def setPredicate(self, predicate):
        self._pedicate = predicate

    def checkNeg(self):
        if self._pedicate.getNeg() and self._pedicate.containsAtribute('_'): return False
        return True

    def checkNotRecursive(self):
        tmp = self._pedicate._predicates
        for p in tmp:
            if p._name == self._pedicate._name: return False

        return True

    def checkSafety(self):
        positiveAtributesSet = {}  # overujem ci negativne boli najskor spomenute v pozitivnom vyzname
        numberOccurenceDic = {}  # overujem ci boli atributy spomenute aspon raz aj v druhej casti

        for a in self._pedicate._atributes:
            numberOccurenceDic[a] = 0

        tmpVerification = Verification(self._tablesSet);

        for p in self._pedicate._atomicPredicates:
            if (not p.checkNeg(tmpVerification)) or not (p._name in self._tablesSet): return False;

            for a in p._atributes:
                if a in numberOccurenceDic:
                    numberOccurenceDic[a] += 1
                else:
                    numberOccurenceDic[a] = 0

                if not p._neg:
                    positiveAtributesSet.add(a)
                else:
                    if not a in positiveAtributesSet: return False

        for a in self._pedicate._atributes:
            if numberOccurenceDic[a] == 0: return False

            # doriesit overovanie conditions
