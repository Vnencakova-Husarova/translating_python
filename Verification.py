class Verification:
    _tablesSet = {}  # set stringov

    def __init__(self, tables):
        self._predicate = []
        self._tablesSet.update(tables)

    def setPredicate(self, predicate):
        self._predicate = predicate

    def checkNeg(self):
        if self._predicate._neg and self._predicate.containsAtribute('_'): return False
        return True

    def checkNotRecursive(self):
        tmp = self._predicate._atomicPredicates
        for p in tmp:
            if p._name == self._predicate._name: return False

        return True

    def checkSafety(self):
        positiveAtributesSet = {}  # overujem ci negativne boli najskor spomenute v pozitivnom vyzname
        numberOccurenceDic = {}  # overujem ci boli atributy spomenute aspon raz aj v druhej casti

        for a in self._predicate._atributes:
            numberOccurenceDic[a] = 0

        tmpVerification = Verification(self._tablesSet);

        for p in self._predicate._atomicPredicates:
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

        for a in self._predicate._atributes:
            if numberOccurenceDic[a] == 0: return False

            # doriesit overovanie conditions
