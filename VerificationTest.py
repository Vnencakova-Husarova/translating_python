import unittest

from Predicate import Predicate
from Verification import Verification


class MyTestCase(unittest.TestCase):
    def test_ver(self):
        tables = {}
        verification = Verification(tables)
        predicate = Predicate('predicate')
        atributes = ['A', 'V']
        predicate1 = Predicate('predicate1')
        predicate2 = Predicate('predicate')
        atributes1 = ['A', 'B']
        atributes2 = ['_', 'C']
        predicate.addAtributes(atributes)
        predicate1.addAtributes(atributes1)
        predicate2.addAtributes(atributes2)
        predicate.addAtomicPredicate(predicate1)
        self.assertEqual(len(predicate._atomicPredicates), 1)
        verification.setPredicate(predicate)
        self.assertEqual(verification.checkNotRecursive(), True)
        predicate.addAtomicPredicate(predicate2)
        self.assertEqual(verification.checkNotRecursive(), False)
        predicate4 = Predicate('predicate')
        atributes4 = ['_', 'B']
        predicate4.addAtributes(atributes4)
        predicate4.negate()
        verification.setPredicate(predicate4)
        self.assertEqual(verification.checkNeg(), False)
        verification.setPredicate(predicate1)
        self.assertEqual(verification.checkNeg(), True)

    def test_safety(self):
        tables = {}
        verification = Verification(tables)
        predicate = Predicate('predicate')
        atributes = ['A', 'V']
        predicate1 = Predicate('predicate1')
        predicate2 = Predicate('predicate2')
        atributes1 = ['A', 'A']
        atributes2 = ['A', 'C']
        predicate.addAtributes(atributes)
        predicate1.addAtributes(atributes1)
        predicate2.addAtributes(atributes2)
        predicate.addAtomicPredicate(predicate1)
        verification.setPredicate(predicate)
        self.assertEqual(verification.checkSafety(), False)
        predicate3 = Predicate('predicate3')
        atributes3 = ['A', 'V']
        predicate3.addAtributes(atributes3)
        predicate.addAtomicPredicate(predicate3)
        self.assertEqual(verification.checkSafety(), True)
        predicate.addAtomicPredicate(predicate2)
        predicate2.negate()
        self.assertEqual(verification.checkSafety(), False)






if __name__ == '__main__':
    unittest.main()
