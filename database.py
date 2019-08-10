import sqlite3
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

    Structure is defined by a dict of str-list of str-str tuples
    Example table and fields would be:

    {
    employees:
        [
            ("text", "first_name"),
            ("text", "last_name"),
            ("integer", "age")
        ]
    wages:
        [
            ("text", "employee_id"),
            ("real", "salary")
        ]
    }
    """
    
    # _structure variable keeps track of the structure of the
    # database it will be modified when adding/removing tables
    # or adding/removing fields
    
    _structure: Dict[str, List[Tuple[str, str]]] = {}
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
        else:
            raise RuntimeError('The database is already initialized')

    def send_query(self, query: str) -> List[Any]:
        """
        Sends and commits a query, returns a list, each element
        of the list is a tuple returned by the database
        """

        self.cursor.execute(query)
        self.db.commit()
        return self.cursor.fetchall()
        
    def create_table(self, table_name: str, table_fields: List[Tuple[str, str]]) -> None:
        """
        Creates a table with fields provided, after that updates _structure
        variable to properly reflect the structure of the database
        """

        q = "CREATE TABLE " + table_name + " (\n\t"
        
        for field in table_fields:
            q = q + field[1] + " " + field[0] + ",\n\t"
        
        q = q[:-3] + "\n\t);"
        self.cursor.execute(q)
        self.db.commit()
        
        self._structure.update({table_name: table_fields})

    def delete_table(self, table_name: str) -> None:
        """
        Looks up the table to be removed in _structure variable
        if found - removes it and drops the table in the database
        else - there is a desync between _structure and the database
        and RuntimeError is raised with appropriate comment
        """
        try:
            self._structure.pop(table_name)
        except KeyError:
            raise RuntimeError("Table to remove not found in structure variable!")

        self.cursor.execute("DROP TABLE " + table_name)
        self.db.commit()

    def get_structure(self) -> Dict[str, List[Tuple[str, str]]]:
        """
        Returns the _structure variable the reflects the current structure
        of the database, _structure is a dictionary with string as a key
        and a list of string-string tuples as a value, key is a name of the
        table and value is a list of fields (1st string is a type, 2nd - name)
        """

        return self._structure

    def save_structure(self) -> None:
        """
        Saves the structure of the database in case it needs to be rebuilt
        however does not save any data
        """

        pass #TODO

    def insert_data(self) -> None:
        """
        Checks and inserts the data if destination exists
        """
        pass #TODO

    def get_data(self) -> None:
        """
        Retrieves data if source exists
        """
        pass #TODO

    def delete_data(self) -> None:
        """
        Wipes the entry if exists
        """
        pass #TODO
