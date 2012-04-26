from database import DBManager
from sqlite3 import connect
import os


class DirectoryManager:
    BASE_DIR = "dbs"

    def __init__(self):
        self.init_DBM = DBManager()

        self.conn = connect(self.BASE_DIR+'/document.db')
        self.c = self.conn.cursor()
        return

    def get_file_path(self, docid):
        self.c.execute("""select parent_dir from document
            where id=?""", (docid,))

        parentid = self.c.fetchone()[0]
        path = ''
        while parentid != 0:
            self.c.execute("""select * from directory
                where id=?""", (parentid,))
            row = self.c.fetchone()
            path = row[1] + '/' + path
            parentid = row[2]
        return path

    def get_dir_path(self, parent_dir):
        parentid = parent_dir
        path = ''
        while parentid != 0:
            self.c.execute("""select * from directory
                where id=?""", (parentid,))
            row = self.c.fetchone()
            path = row[1] + '/' + path
            parentid = row[2]
        return path

    def get_file_path_physical(self, docid):
        self.c.execute("""select parent_dir from document
            where id=?""", (docid,))

        parentid = self.c.fetchone()[0]
        path = ''
        while parentid != 0:
            self.c.execute("""select * from directory
                where id=?""", (parentid,))
            row = self.c.fetchone()
            path = '%s/%s' % (row[0], path)
            parentid = row[2]
        return path

    def get_dir_path_physical(self, parent_dir):
        parentid = parent_dir
        path = ''
        while parentid != 0:
            self.c.execute("""select * from directory
                where id=?""", (parentid,))
            row = self.c.fetchone()
            path = '%s/%s' % (row[0], path)
            parentid = row[2]
        return path

    def get_directory_id(self, name, parent_dir):
        self.c.execute("""select id from directory where
            lower(name)=? and parent_dir=?""", (name.lower(), parent_dir))
        res = self.c.fetchone()

        if res != None:
            return True, res[0]
        else:
            return False,

    def add_directory(self, name, parent_dir):
        dirid = self.get_directory_id(name, parent_dir)

        if dirid[0]:
            return False, dirid[1]

        t = (name, parent_dir)
        self.c.execute("""insert into directory values (
            NULL, ?, ? )""", t)

        self.conn.commit()
        return self.get_directory_id(name, parent_dir)

    def create_directory(self, dirid, parent_dir):
        path = self.get_dir_path_physical(parent_dir)

        if not os.path.isdir('%s%s' % (path, dirid)):
            os.mkdir('%s%s' % (path, dirid))
            return True
        else:
            return False

    def get_dir_dir(self, parent_dir):
        self.c.execute("""select * from directory where parent_dir=?""", (parent_dir,))

        res = []
        for row in self.c:
            res.append({'id': row[0], 'name': row[1], 'parent_dir': row[2]})

        return res
