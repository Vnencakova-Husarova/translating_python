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
        tables = {'predicate1', 'predicate2', 'predicate3'}
        verification = Verification(tables)
        predicate = Predicate('predicate')
        atributes = ['A', 'V']
        predicate1 = Predicate('predicate1')
        predicate2 = Predicate('predicate2')
        atributes1 = ['A', 'A']
        atributes2 = ['A', 'C']
        predicate.add_atributes(atributes)
        predicate1.add_atributes(atributes1)
        predicate2.add_atributes(atributes2)
        predicate.add_atomic_predicate(predicate1)
        verification.set_predicate(predicate)
        self.assertEqual(verification.check_safety(), False)
        predicate3 = Predicate('predicate3')
        atributes3 = ['A', 'V']
        predicate3.add_atributes(atributes3)
        predicate.add_atomic_predicate(predicate3)
        self.assertEqual(verification.check_safety(), True)
        predicate.add_atomic_predicate(predicate2)
        predicate2.negate()
        self.assertEqual(verification.check_safety(), False)


if __name__ == '__main__':
    unittest.main()
