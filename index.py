from database import DBManager
from sqlite3 import connect
from porter import PorterStemmer


class IndexManager:
    BASE_DIR = "dbs"

    def __init__(self):
        self.init_DBM = DBManager()

        self.conn = connect(self.BASE_DIR+'/index.db')
        self.c = self.conn.cursor()
        return

    def add_index_word(self, word, docid, line, column):
        res = self.get_index_word_id(word)

        if not res[0]:
            self.c.execute("""insert into index_word values (
                NULL, ? )""", (word,))
            wordid = self.get_index_word_id(word)[1]
        else:
            wordid = res[1]

        res = self.get_index_ref_id(wordid, docid, line, column)
        if not res[0]:
            self.c.execute("""insert into index_ref values (
                NULL, ?, ?, ?, ? )""", (wordid, docid, line, column))

        self.conn.commit()
        return True, wordid

    def get_index_word_id(self, word):
        self.c.execute("""select id from index_word where
            word=? """, (word,))
        res = self.c.fetchone()

        if res != None:
            return True, res[0]
        else:
            return False,

    def get_index_word(self, wordid):
        self.c.execute("""select word from index_word where
            id=? """, (wordid,))
        res = self.c.fetchone()

        if res != None:
            return True, res[0]
        else:
            return False, ''

    def get_index_ref_id(self, wordid, docid, line, col):
        self.c.execute("""select id from index_ref where
            wordid=? AND docid=? AND line=? AND column=?""",
            (wordid, docid, line, col))
        res = self.c.fetchone()

        if res != None:
            return True, res[0]
        else:
            return False,

    def search(self, word):
        PS = PorterStemmer()

        wordid = self.get_index_word_id(PS.stem(word, 0, len(word)-1))

        res = []
        if wordid[0]:
            self.c.execute("""select * from index_ref where
                wordid=?""", (wordid[1],))
            l = self.c.fetchall()
            for row in l:
                res.append({
                    'id': row[0],
                    'word': self.get_index_word(row[1])[1],
                    'docid': row[2],
                    'doc': self.init_DBM.get_document_info(row[2])['name'],
                    'line': row[3],
                    'column': row[4]})
        return res
