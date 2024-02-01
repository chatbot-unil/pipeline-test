import sqlite3

class Data:
    def __init__(self, path, init=False, path_init=None):
        self.db = sqlite3.connect(path)
        if init:
            self.init_db(path_init)

    def init_db(self, db):
        with open(db, 'r') as f:
            self.db.cursor().executescript(f.read())
        self.db.commit()

    def disconnect(self):
        self.db.close()

    def execute(self, query, values=None):
        if values:
            self.db.cursor().execute(query, values)
        else:
            self.db.cursor().execute(query)
        self.db.commit()

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
    
    async def get_file(self, file_id: str):
        query = "SELECT * FROM Files WHERE files_id = :file_id"
        values = {
            "file_id": file_id,
        }
        return await self.fetch_one(query=query, values=values)
    
    async def add_file_to_current(self, file_id: str):
        query = "INSERT INTO CurrentUseFiles (files_id) VALUES (:file_id)"
        values = {
            "file_id": file_id,
        }
        return await self.execute(query=query, values=values)
    
    async def get_current_files(self):
        query = "SELECT * FROM CurrentUseFiles"
        return await self.fetch_all(query=query)
    
    async def delete_current_files(self):
        query = "DELETE FROM CurrentUseFiles"
        return await self.execute(query=query)
    
    async def get_all_files(self):
        query = "SELECT * FROM Files"
        return await self.fetch_all(query=query)    
    
    async def get_all_files_by_type(self, type_id: int):
        query = "SELECT * FROM Files WHERE type_id = :type_id"
        values = {
            "type_id": type_id,
        }
        return await self.fetch_all(query=query, values=values)
    
    async def truncate_files(self):
        query = "DELETE FROM Files"
        return await self.execute(query=query)
    
    async def truncate_current_files(self):
        query = "DELETE FROM CurrentUseFiles"
        return await self.execute(query=query)
    
    async def truncate_all(self):
        await self.truncate_files()
        await self.truncate_current_files()