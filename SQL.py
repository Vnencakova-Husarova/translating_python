from Parser import Parser
from Table import Table


class SQL:
    def __init__(self, string, database):
        self._string = string
        self._database = database
        self._predicates = []

    def parse(self):
        parser = Parser(self._string)
        self._predicates = parser.parse()

    def translate_one(self, predicate):
        _main = ''
        _select = ''
        _from = ''
        _where = ''

        tmp = False
        _main += 'CREATE TEMPORARY TABLE ' + predicate._name + ' AS '
        columns = []

        #domysliet ci netreba premenovavat stlpceky v pomocnych, ako tvorit nove tabulky

        _select += '\n SELECT '

        iC = 0
        for atribute in predicate._atributes:
            iC += 1
            iS = 0
            if tmp:
                _select += ', '
            for p in predicate._atomic_predicates:
                iS += 1
                if not p._neg and p.contains_atribute(atribute):
                    _select += p._name + '_' + str(iS) + '.'
                    tmp_index = p.index_of(atribute)
                    _select += ((self._database).get_table(p._name)).get_column(tmp_index)
                    _select += ' AS column_' + str(iC)
                    columns.append('column_' + str(iC))
                    break

              #  iS += 1

            tmp = True

        _from += '\n FROM '
        iF = 0
        tmp = False
        for p in predicate._atomic_predicates:
            iF += 1
            if p._neg:
                break
            if tmp:
                _from += ', '
            _from += p._name + ' ' + p._name + '_' + str(iF)
            tmp = True

        _where += '\n WHERE '
        tmp = False

        for comparison in p._atomic_comparisons:
            if tmp:
                _where += ' AND '
            _where += comparison.to_string()
            tmp = True

        used = set()
        tmp_predicates = predicate._atomic_predicates
        for i in range(0, len(tmp_predicates)):
            tmp_atributes = tmp_predicates[i]._atributes

            for l in range(0, len(tmp_atributes)):
                if tmp_atributes[l] in used:
                    continue

                if tmp_atributes[l] == '_':
                    continue

                for k in range(i + 1, len(tmp_predicates)):

                    if (not tmp_predicates[k]._neg) and tmp_predicates[k].contains_atribute(tmp_atributes[l]):
                        if tmp:
                            _where += ' AND '
                        _where += tmp_predicates[i]._name + '_' + str(i + 1) + '.'
                        _where += self._database.get_table(tmp_predicates[i]._name).get_column(l)
                        _where += ' = ' + tmp_predicates[k]._name + '_' + str(k + 1) + '.'
                        index = tmp_predicates[k].index_of(tmp_atributes[l])
                        _where += self._database.get_table(tmp_predicates[k]._name).get_column(index)
                        tmp = True


                used.add(tmp_atributes[l])

        _negation = ''

        for i in range(0, len(tmp_predicates)):
            if not tmp_predicates[i]._neg:
                continue

            if tmp:
                _where += ' AND '
            _negation += '\n NOT EXISTS (SELECT * FROM ' + tmp_predicates[i]._name + ' '
            tmp_name = tmp_predicates[i]._name + '_' + str(iF)
            _negation += tmp_name + ' WHERE '
            iF += 1
            atribute_list = tmp_predicates[i]._atributes
            tmp2 = False

            for l in range(0, len(atribute_list)):
                if atribute_list[l] == '_':
                    continue
                for k in range(0, i):
                    if (not tmp_predicates[k]._neg) and tmp_predicates[k].contains_atribute(atribute_list[l]):
                        if tmp2:
                            _negation += ' AND '
                        _negation += tmp_name + '.'
                        _negation += self._database.get_table(tmp_predicates[i]._name).get_column(l)
                        _negation += ' = ' + tmp_predicates[k]._name + '_' + str(k + 1) + '.'
                        index = tmp_predicates[k].index_of(atribute_list[l])
                        _negation += self._database.get_table(tmp_predicates[k]._name).get_column(index)
                        tmp2 = True

            _negation += ' ) '

        _select += _from + _where + _negation + ';'
        _main += _select

        self._database.add_table(Table(predicate._name, columns))
        return _main






