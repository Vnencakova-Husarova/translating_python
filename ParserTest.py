import unittest

from Parser import Parser


class MyTestCase(unittest.TestCase):
    def test_spaces(self):
        parser = Parser('    a  ')
        self.assertEqual(parser.i, 0)
        parser.spaces()
        self.assertEqual(parser.i, 4)
        parser.i += 1
        parser.spaces()
        self.assertEqual(parser.i, 7)

    def test_readName(self):
        parser = Parser('lalala ahoj')
        self.assertEqual(parser.readName(parser._charsPredicate), 'lalala')
        self.assertEqual(parser.i, 6)
        self.assertEqual(parser.readName(parser._charsPredicate), 'ahoj')
        self.assertEqual(parser.i, 11)

    def test_readPredicate(self):
        parser = Parser('predicate(A, B, C)')
        atr = ['A', 'B', 'C']
        predicate = parser.readPredicate(False, False)
        self.assertEqual(predicate._name, 'predicate')
        self.assertEqual(atr, predicate._atributes)
        parser2 = Parser('predicate(A, _, C)')
        predicate2 = parser2.readPredicate(False, True)
        self.assertEqual(predicate2, None)
        parser3 = Parser('predicateA(A, _, C)')
        predicate3 = parser3.readPredicate(True, False)
        self.assertEqual(predicate3._name, 'predicateA')
        self.assertEqual(predicate3._neg, True)
        parser4 = Parser('\+ p(A, B)')
        predicate4 = parser4.readNext()
        self.assertEqual(predicate4._name, 'p')
        self.assertEqual(predicate4._neg, True)
        self.assertEqual(predicate4._atributes, ['A', 'B'])


    def test_readLine(self):
        parser = Parser('p(A, B) :- pred(A, C), r(A, C).')
        predicate = parser.parseLine()
        self.assertEqual(predicate._name, 'p')
        self.assertEqual(predicate._atributes, ['A', 'B'])
        self.assertEqual(len(predicate._atomicPredicates), 2)
        self.assertEqual(predicate._atomicPredicates[1]._name, 'r')
        self.assertEqual(predicate._atomicPredicates[0]._atributes, ['A', 'C'])
        parser1 = Parser('p(A, _) :- pred(A, C), r(A, C).')
        predicate1 = parser1.parseLine()
        self.assertEqual(predicate1, None)
        parser2 = Parser('p(A) :-- pred(A, C), r(A, C).')
        predicate2 = parser2.parseLine()
        self.assertEqual(predicate2, None)

    def test_parse(self):
        parser = Parser('p(A, B) :- pred(A, C), r(A, C).'
                        's(D) :- p(A, _), pred(A, C), r(A, C).')
        listOfPredicates = parser.parse()
        self.assertEqual(len(listOfPredicates), 2)
        self.assertEqual(listOfPredicates[0]._name, 'p')
        self.assertEqual(listOfPredicates[1]._name, 's')
        self.assertEqual(listOfPredicates[0]._atomicPredicates[1]._name, 'r')
        self.assertEqual(listOfPredicates[1]._atomicPredicates[1]._name, 'pred')
        self.assertEqual(listOfPredicates[1]._atomicPredicates[2]._atributes, ['A', 'C'])
        parser2 = Parser('p(A, B) :- pred(A, C), r(A, C). '
                        's(D) :- p(A, _), pred(A, C), r(A, C)')
        listOfPredicates2 = parser2.parse()
        self.assertEqual(listOfPredicates2, None)



if __name__ == '__main__':
    unittest.main()
