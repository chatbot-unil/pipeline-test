import sqlite3

class Data:
    _instance = None  # Class attribute that stores the singleton instance

    def __new__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super(Data, self).__new__(self)
            # Put any initialization here that should only happen once
        return self._instance

    def __init__(self, path, path_init=None):
        # Prevent re-initialization if the __init__ is called more than once
        if not hasattr(self, 'db'):
            self.db = sqlite3.connect(path)
            self.init_db(path_init)

    def init_db(self, path_init):
        if self.db is not None:
            self.truncate_all()
        else:
            if path_init:
                with open(path_init, 'r') as f:
                    self.db.executescript(f.read())
            self.db.commit()

    def disconnect(self):
        self.db.close()

    def execute(self, query, values=None):
        if values:
            self.db.cursor().execute(query, values)
        else:
            self.db.cursor().execute(query)
        self.db.commit()

    def fetch_one(self, query, values=None):
        if values:
            return self.db.cursor().execute(query, values).fetchone()
        else:
            return self.db.cursor().execute(query).fetchone()
    
    def fetch_all(self, query, values=None):
        if values:
            return self.db.cursor().execute(query, values).fetchall()
        else:
            return self.db.cursor().execute(query).fetchall()

    def add_file(self, file_id: str, file_name: str, type_id: int):
        query = "INSERT INTO Files (files_id, file_name, type_id) VALUES (:file_id, :file_name, :type_id)"
        values = {
            "file_id": file_id,
            "file_name": file_name,
            "type_id": type_id,
        }
        self.execute(query=query, values=values)
    
    def add_root_file(self, file_id: str, file_name: str):
        query = "INSERT INTO Files (files_id, file_name, type_id) VALUES (:file_id, :file_name, 3)"
        values = {
            "file_id": file_id,
            "file_name": file_name,
        }
        self.execute(query=query, values=values)

    def get_file(self, file_id: str):
        query = "SELECT * FROM Files WHERE files_id = :file_id"
        values = {
            "file_id": file_id,
        }
        return self.fetch_one(query=query, values=values)
    
    def add_file_to_current(self, file_id: str):
        query = "INSERT INTO CurrentUseFiles (files_id) VALUES (:file_id)"
        values = {
            "file_id": file_id,
        }
        self.execute(query=query, values=values)

    def get_all_files(self):
        query = "SELECT * FROM Files"
        return self.fetch_all(query=query)
    
    def truncate_current_files(self):
        query = "DELETE FROM CurrentUseFiles"
        self.execute(query=query)
    
    def truncate_files(self):
        query = "DELETE FROM Files"
        self.execute(query=query)

    def truncate_all(self):
        self.truncate_files()
        self.truncate_current_files()
    
    def get_current_files(self):
        query = "SELECT * FROM CurrentUseFiles"
        return self.fetch_all(query=query)
    
    def delete_current_files(self):
        query = "DELETE FROM CurrentUseFiles"
        self.execute(query=query)

    def delete_file(self, file_id: str):
        query = "DELETE FROM Files WHERE files_id = :file_id"
        values = {
            "file_id": file_id,
        }
        self.execute(query=query, values=values)

    def get_all_files_by_type(self, type_id: int):
        query = "SELECT * FROM Files WHERE type_id = :type_id"
        values = {
            "type_id": type_id,
        }
        return self.fetch_all(query=query, values=values)