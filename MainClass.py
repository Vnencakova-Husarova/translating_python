from Database import Database
from Parser import Parser
from SQL import SQL
from Table import Table
from Verification import Verification


def main():
    from_text_window = 'aaaabbbb(B, C) : - pristupova_karta(B, C).'
    parser = Parser(from_text_window)
    array_of_predicates = parser.parse()
    if array_of_predicates is None:
        print(parser.get_problem())
        return 0

    tmp_set = {'student', 'zamestnanec', 'pristupova_karta', 'navsteva', 'miestnost',
                'obsah_priecinka', 'absolvoval', 'vyucuje', 'otvoreny_subor_na_pocitaci',
                'miestnost_pocitac', 'historia_vyhladavania'}
    verification = Verification(tmp_set)

    for predicate in array_of_predicates:
        predicate.check_whole(verification)
        print(verification.get_problem())

    tables = {Table('student', ['id', 'meno', 'priezvisko', 'rocnik', 'nickname']),
              Table('zamestnanec', ['id', 'meno', 'priezvisko']),
              Table('pristupova_karta', ['id', 'id_majitela']),
              Table('navsteva', ['id_karty', 'id_miestnosti', 'cas_od', 'cas_do']),
              Table('miestnost', ['id', 'nazov']),
              Table('obsah_priecinka', ['nazov_priecinka', 'nazov_suboru']),
              Table('absolvoval', ['id_studenta', 'predmet']),
              Table('vyucuje', ['id_ucitela', 'predmet']),
              Table('otvoreny_subor_na_pocitaci', ['nazov_suboru', 'id_pocitaca', 'skompilovany']),
              Table('miestnost_pocitac', ['id_miestnosti', 'id_pocitaca']),
              Table('historia_vyhladavania', ['id_uzivatel', 'predmet_vyhladavania', 'cas'])}

    database = Database(tables)
    sql = SQL(array_of_predicates, database)
    result_to_sql = sql.translate_all()
    print(result_to_sql)


if __name__ == "__main__":
    main()