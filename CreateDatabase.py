from Database import Database


class CreateDatabase:
    _database = False

    def __init__(self, tables):
        if not self._database:
            self._instance = Database(tables)
            self._database = True

    def get_database(self):
        return self._instance
