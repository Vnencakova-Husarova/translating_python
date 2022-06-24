import unittest

from Predicate import Predicate


class MyTestCase(unittest.TestCase):
    def test_class(self):
        atributes = ['A', 'B', 'C']
        atributesNew = ['A', 'B', 'C', 'D']

        predicate = Predicate('predicate1')
        predicate.add_atributes(atributes)
        predicate.add_atribute('D')

        self.assertEqual(predicate._atributes, atributesNew)
        self.assertEqual(predicate._neg, False)
        predicate.negate()
        self.assertEqual(predicate._neg, True)
        self.assertEqual(predicate.index_of('A'), 0)
        self.assertEqual(predicate.index_of('C'), 2)


if __name__ == '__main__':
    unittest.main()
