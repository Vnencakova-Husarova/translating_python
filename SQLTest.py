import unittest

from CreateDatabase import CreateDatabase
from Parser import Parser
from SQL import SQL
from Table import Table


class MyTestCase(unittest.TestCase):
    def test_translate_one(self):
        parser = Parser('vypilOblubeny(P, A) :- lubi(P, A), navstivil(P, _, I), vypil(I, A, _).')
        parser2 = Parser('vypilNeblubeny(P, A) :-  navstivil(P, _, I), vypil(I, A, _), \+ lubi(P, A).')

        t_v = Table('vypil', ['id', 'alkohol', 'mnozstvo'])
        t_l = Table('lubi', ['pijan', 'alkohol'])
        t_n = Table('navstivil', ['pijan', 'krcma', 'id'])

        database = CreateDatabase({t_v, t_n, t_l})
        tmp = database.get_database()
        sql = SQL('', tmp)

        predicate = parser.parse_line()
        predicate2 = parser2.parse_line()
        print(sql.translate_one(predicate) + '\n')
        print(sql.translate_one(predicate2) + '\n')

if __name__ == '__main__':
    unittest.main()
