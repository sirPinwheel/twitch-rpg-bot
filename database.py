import sqlite3
import pickle
from typing import Any, List, Tuple, Dict

class Database():
    """
    Class wrapping the sqlite3 database instance, provides
    an interface for saving and retrieving data
    
    Avilable types:
    +----------+----------+
    | SQLITE   | PYTHON   |
    +----------+----------+
    | null     | None     |
    | integer  | int      |
    | real     | float    |
    | text     | str      |
    | blob     | buffer   |
    +----------+----------+
    """

    _instance: Any = None

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
            self._send_query(
                    "CREATE TABLE players (username text, data text)"
                )
        else:
            raise RuntimeError('The database is already initialized')

    def _send_query(self, query: str) -> List[Any]:
        """
        Sends and commits a query, returns a list, each element
        of the list is a tuple returned by the database
        """

        self.cursor.execute(query)
        self.db.commit()
        return self.cursor.fetchall()

    def insert_data(self, user: str, data: Any) -> None:
        """
        Checks and inserts the data if destination exists
        """
        serialized: str = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
        
        self.cursor.execute(
            "INSERT INTO players (username, data) VALUES (?, ?)", [user, sqlite3.Binary(serialized)]
        )
        self.db.commit()

    def get_data(self, user: str) -> Any:
        """
        Retrieves data if source exists
        """

        self.cursor.execute("SELECT * FROM players WHERE username=?", [user])
        self.db.commit()

        retrieved_data: str = self.cursor.fetchall()
        
        if retrieved_data != []: return pickle.loads(retrieved_data[0][1])
        else: return None

    def delete_data(self, user: str) -> None:
        """
        Wipes the entry if exists
        """

        self.cursor.execute("DELETE FROM players WHERE username=?", [user])
        self.db.commit()
