
class Database:
    _tables = set()
    _tables_names = set()

    def __init__(self, tables):
        self._tables = tables
        self._temporary_tables = set()
        self._tables_names = set()
        self._temporary_tables_names = set()

    def add_table(self, table):
        self._tables.add(table)
        self._tables_names.add(table._name)

    def add_temporary_table(self, table):
        self._tables.add(table)
        self._tables_names.add(table._name)
        self._temporary_tables.add(table)
        self._temporary_tables_names.add(table._name)


    def get_table(self, name):
        for t in self._tables:
            if t._name == name:
                return t

        return None

    def remove_temporary_tables(self):
        self._tables.difference_update(self._temporary_tables)
        self._tables_name.difference_update(self._temporary_tables_names)


