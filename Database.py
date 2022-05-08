
class Database:
    _tables = set()

    def __init__(self, tables):
        self._tables = tables

    def add_table(self, table):
        self._tables.add(table)

    def get_table(self, name):
        for t in self._tables:
            if t._name == name:
                return t

        return None


