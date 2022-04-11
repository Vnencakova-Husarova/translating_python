import singleton as singleton


@singleton
class Database:
    def __init__(self, tables):
        self._tables = tables

pass

class CreateDatabase:
    _instance = None

    def __init__(self, tables):
        if self._instance == None:
             self._instance = Database(tables)
        return self._instance

    def addTable(self, table):
        table.update(table)

    def getTable(self, name):
        for t in self._tables:
            if t._name == name: return t
        return None