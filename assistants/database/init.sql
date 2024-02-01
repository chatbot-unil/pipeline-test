CREATE TABLE IF NOT EXISTS FileType (
    type_id INTEGER PRIMARY KEY,
    type_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Files (
    files_id TEXT PRIMARY KEY,
    file_name TEXT NOT NULL,
    type_id INTEGER,
    FOREIGN KEY (type_id) REFERENCES FileType(type_id)
);

CREATE TABLE IF NOT EXISTS CurrentUseFiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    files_id INTEGER,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO FileType (type_id, type_name) VALUES (1, 'DATA');
INSERT INTO FileType (type_id, type_name) VALUES (2, 'ACCES_INFO');
INSERT INTO FileType (type_id, type_name) VALUES (3, 'ROOT');