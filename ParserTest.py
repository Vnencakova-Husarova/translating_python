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
        self.assertEqual(parser.read_name(parser._chars_predicate), 'lalala')
        self.assertEqual(parser.i, 6)
        self.assertEqual(parser.read_name(parser._chars_predicate), 'ahoj')
        self.assertEqual(parser.i, 11)

    def test_readPredicate(self):
        parser = Parser('predicate(A, B, C)')
        atr = ['A', 'B', 'C']
        predicate = parser.read_predicate(False, False)
        self.assertEqual(predicate._name, 'predicate')
        self.assertEqual(atr, predicate._atributes)
        parser2 = Parser('predicate(A, _, C)')
        predicate2 = parser2.read_predicate(False, True)
        self.assertEqual(predicate2, None)
        parser3 = Parser('predicateA(A, _, C)')
        predicate3 = parser3.read_predicate(True, False)
        self.assertEqual(predicate3._name, 'predicateA')
        self.assertEqual(predicate3._neg, True)
        parser4 = Parser('\+ p(A, B)')
        predicate4 = parser4.read_next()
        self.assertEqual(predicate4._name, 'p')
        self.assertEqual(predicate4._neg, True)
        self.assertEqual(predicate4._atributes, ['A', 'B'])

    def test_readCond(self):
        parser = Parser('A = B')
        comparison = parser.read_condition(False)
        self.assertEqual(comparison.is_second_int(), False)
        self.assertEqual(comparison._second, 'B')
        parser1 = Parser('A = 50')
        com2 = parser1.read_condition(False)
        self.assertEqual(com2.is_second_int(), True)
        self.assertEqual(com2._second, '50')






    def test_readLine(self):
        parser = Parser('p(A, B) :- pred(A, C), r(A, C).')
        predicate = parser.parse_line()
        self.assertEqual(predicate._name, 'p')
        self.assertEqual(predicate._atributes, ['A', 'B'])
        self.assertEqual(len(predicate._atomic_predicates), 2)
        self.assertEqual(predicate._atomic_predicates[1]._name, 'r')
        self.assertEqual(predicate._atomic_predicates[0]._atributes, ['A', 'C'])
        parser1 = Parser('p(A, _) :- pred(A, C), r(A, C).')
        predicate1 = parser1.parse_line()
        self.assertEqual(predicate1, None)
        parser2 = Parser('p(A) :-- pred(A, C), r(A, C).')
        predicate2 = parser2.parse_line()
        self.assertEqual(predicate2, None)

    def test_parse(self):
        parser = Parser('p(A, B) :- pred(A, C), r(A, C).'
                        's(D) :- p(A, _), pred(A, C), r(A, C).')
        listOfPredicates = parser.parse()
        self.assertEqual(len(listOfPredicates), 2)
        self.assertEqual(listOfPredicates[0]._name, 'p')
        self.assertEqual(listOfPredicates[1]._name, 's')
        self.assertEqual(listOfPredicates[0]._atomic_predicates[1]._name, 'r')
        self.assertEqual(listOfPredicates[1]._atomic_predicates[1]._name, 'pred')
        self.assertEqual(listOfPredicates[1]._atomic_predicates[2]._atributes, ['A', 'C'])
        parser2 = Parser('p(A, B) :- pred(A, C), r(A, C). '
                        's(D) :- p(A, _), pred(A, C), r(A, C)')
        listOfPredicates2 = parser2.parse()
        self.assertEqual(listOfPredicates2, None)



if __name__ == '__main__':
    unittest.main()
