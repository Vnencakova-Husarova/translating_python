class Table:
    def __init__(self, name, columns):
        self._name = name
        self._columns.extend(columns)

    def get_name(self):
        return self._name

    def get_column(self, i):
        return self._columns[i]