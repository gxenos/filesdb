import sqlite3


class DataBase:
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS scan(
              ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
              DATE DATE NOT NULL DEFAULT CURRENT_DATE,
              FOLDER_SCANNED TEXT NOT NULL,
              TYPE TEXT NOT NULL
        );''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS file(
              ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
              NAME TEXT NOT NULL,
              SIZE TEXT NOT NULL,
              PATH TEXT NOT NULL,
              MD5 CHAR(32) DEFAULT NULL,
              SHA1 CHAR(40) DEFAULT NULL,
              XX32 CHAR(8) DEFAULT NULL,
              XX64 CHAR(16) DEFAULT NULL,
              SSDEEP CHAR(16) DEFAULT NULL,
              BASENAME TEXT NOT NULL,
              EXTENSION TEXT,
              DIRECTORY TEXT,
              READ BOOLEAN,
              WRITE BOOLEAN,
              EXECUTE BOOLEAN,
              SCAN_ID INTEGER NOT NULL,
              FOREIGN KEY (SCAN_ID) REFERENCES scan(ID)
        );''')

    def add_scan(self, folder):
        query = '''INSERT INTO scan(FOLDER_SCANNED, TYPE) VALUES(?, 'Full Scan');'''
        self.cursor.execute(query, (folder,))

    def add_quick_scan(self, folder):
        query = '''INSERT INTO scan(FOLDER_SCANNED, TYPE) VALUES(?, 'Quick Scan');'''
        self.cursor.execute(query, (folder,))

    def get_last_scan_id(self):
        query = '''SELECT * FROM scan ORDER BY ID DESC LIMIT 1;'''
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def add_file(self, file, scan_id):
        query = '''INSERT INTO file(NAME,SIZE, PATH,MD5,SHA1,XX32,XX64,SSDEEP,BASENAME,EXTENSION,DIRECTORY,READ,WRITE,EXECUTE,SCAN_ID) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        self.cursor.execute(query, file.get_tuple() + (scan_id,))

    def add_quick_file(self, file, scan_id):
        query = '''INSERT INTO file(NAME,SIZE, PATH,BASENAME,EXTENSION,DIRECTORY,READ,WRITE,EXECUTE,SCAN_ID) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        self.cursor.execute(query, file.get_quick_tuple() + (scan_id,))

    def print_all(self):
        self.cursor.execute('''SELECT * FROM file''')
        return self.cursor

    def list_scans(self):
        self.cursor.execute('''SELECT * FROM scan''')
        return self.cursor

    def show_stats(self):
        self.cursor.execute('''SELECT SCAN_ID, COUNT(*) FROM file GROUP BY SCAN_ID''')
        return self.cursor

    def dissconect(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


def main():
    db = DataBase('files.db')
    print(db.list_scans())
    db.dissconect()

if __name__ == '__main__':
    main()
