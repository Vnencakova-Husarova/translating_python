class Table:
    def __init__(self, name, columns):
        self._name = name
        self._columns.extend(columns)

    def getName(self):
        return self._name

    def getColumn(self, i):
        return self._columns[i]