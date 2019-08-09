import sqlite3
from typing import Any, List

class Database:
    """
    Class wrapping the sqlite3 database instance, provides
    an interface for saving and retrieving user characters
    """

    _instance = None

    def __new__(self):
        if self._instance == None:
            self._instance = super(Database, self).__new__(self)
            self.db: Any = None
            self.cursor: Any = None

        return self._instance

    def __del__(self):
        if self.db is not None:
            self.db.close()

    def initialize(self, filename: str="") -> None:
        """
        Opens connection to local database and creates a cursor.
        If no filename provided, the database will be created
        in memory and get destroyed upon exiting the program
        """
        
        if self.db == None:
            if filename == "":
                self.db = sqlite3.connect(":memory:")
            else:
                self.db = sqlite3.connect(filename)

            self.cursor = self.db.cursor()
        else:
            raise RuntimeError('The database is already initialized')

    def send_query(self, query: str) -> List[Any]:
        """
        Sends and commits a query, returns a list, each element
        of the list is a line returned by the database from
        first to last
        """

        self.cursor.execute(query)
        self.db.commit()
        return self.cursor.fetchall()
        