from database import DBManager
from directory import DirectoryManager
from index import IndexManager
from porter import PorterStemmer
from time import time
from sqlite3 import connect
import user
import os
import re


class Document:
    BASE_DIR = "dbs"

    def __init__(self, ID):
        self.manage_DB = DBManager()
        self.manage_Docs = DocumentManager(self.manage_DB)
        self.manage_Indx = IndexManager()

        self.conn = connect(self.BASE_DIR+'/document.db')
        self.c = self.conn.cursor()

        self.info = self.manage_DB.get_document_info(ID)
        self.info['lpath'] = self.manage_Docs.get_file_path(self.info['id'])
        self.info['ppath'] = self.manage_Docs.get_file_path_physical(
            self.info['id'])
        return

    def is_memeber(self, userid):
        if self.info['owner'] == userid:
            return True

        self.c.execute("""select * from member where
            docid=? and userid=?""",
            (self.info['id'], userid))
        res = self.c.fetchone()

        if res:
            return True
        else:
            return False

    def get_invitation_id(self, userid_from, userid_to):
        self.c.execute("""select id from invitation where
            docid=? and userid_from=? and userid_to=?""",
            (self.info['id'], userid_from, userid_to))
        res = self.c.fetchone()

        if res != None:
            return True, res[0]
        else:
            return False,

    def get_comment_id(self, userid, content):
        self.c.execute("""select id from comment where
            docid=? and userid=? and content=?""",
            (self.info['id'], userid, content))
        res = self.c.fetchone()

        if res != None:
            return True, res[0]
        else:
            return False,

    def get_complaint_id(self, userid):
        self.c.execute("""select id from complaint where
            docid=? and userid=? """,
            (self.info['id'], userid))
        res = self.c.fetchone()

        if res != None:
            return True, res[0]
        else:
            return False,

    def insert_invitation(self, userid_from, userid_to, content):
        inviteid = self.get_invitation_id(userid_from, userid_to)

        if inviteid[0]:
            return False, inviteid[1]

        self.c.execute("""insert into invitation values (
            NULL, ?, ?, ?, ?, ?, 0)""",
            (self.info['id'], userid_from, userid_to, content, time()))

        self.conn.commit()
        return self.get_invitation_id(userid_from, userid_to)

    def insert_comment(self, userid, content):
        commentid = self.get_comment_id(userid, content)

        if commentid[0]:
            return False, commentid[1]

        self.c.execute("""insert into comment values (
            NULL, ?, ?, ?, ? )""",
            (self.info['id'], userid, content, time()))

        self.conn.commit()
        return self.get_comment_id(userid, content)

    def insert_complaint(self, userid, content):
        complaintid = self.get_complaint_id(userid)

        if complaintid[0]:
            return False, complaintid[1]

        self.c.execute("""insert into complaint values (
            NULL, ?, ?, ?, ?, 0 )""",
            (self.info['id'], userid, content, time()))

        self.conn.commit()
        return self.get_complaint_id(userid)

    def view_comments(self):
        self.c.execute("""select * from comment where docid=?""",
            (self.info['id'], ))

        res = []
        for row in self.c:
            res.append({'id': row[0], 'docid': row[1], 'userid': row[2],
                'content': row[3], 'time': row[4]})

        return res

    def view_complaints(self):
        self.c.execute("""select * from complaint where docid=?""",
            (self.info['id'], ))

        res = []
        for row in self.c:
            res.append({'id': row[0], 'docid': row[1], 'userid': row[2],
                'content': row[3], 'time': row[4]})

        return res

    def index_document(self):
        fhandle = open(self.info['ppath'] + str(self.info['id']), 'r')
        PS = PorterStemmer()

        content = fhandle.readline().lower()
        line_count = 1
        while content != '':
            words = re.findall('\w+', content)
            for word in words:
                if len(word) > 3:
                    col_count = content.find(word) + 1
                    self.manage_Indx.add_index_word(
                        PS.stem(word, 0, len(word)-1),
                        self.info['id'],
                        line_count,
                        col_count)
            content = fhandle.readline().lower()
            line_count += 1

        fhandle.close()
        return

    def create_autocompleteDB(self, content):
        if not os.path.exists(self.BASE_DIR+'/autocomplete.db'):
            f = open(self.BASE_DIR+'/autocomplete.db', 'w')
            f.close()

        conn = connect(self.BASE_DIR+'/autocomplete.db')
        c = conn.cursor()

        if not self.manage_DB.check_DB_exist(conn, str(self.info['id'])):
            c.execute("""create table ? (
                id integer primary key autoincrement,
                word text)""", (self.info['id'],))

            words = re.findall('\w+', content).lower()
            for word in words:
                if len(word) > 3:
                    conn.execute("""insert into ? values (
                        NULL, ?)""", (self.info['id'],))

            conn.commit()
        return

    def suggest_autocomplete(self, fragment):
        conn = connect(self.BASE_DIR+'/autocomplete.db')
        c = conn.cursor()

        c.execute("""select * where word Like ?""", (fragment+'%',))

        res = []
        for row in c:
            res.append({'id': row[0], 'word': row[1]})

        return res


class DocumentManager:
    BASE_DIR = "dbs"

    def __init__(self, dbm):
        # Save an instance of the database manager.
        self.manage_DB = dbm

        # Create a connection to the document database.
        self.conn = connect(self.BASE_DIR+'/document.db')
        self.c = self.conn.cursor()
        return

    def create_document(self, docid, parent_dir):
        # Get the local file system path for the supplied parent_dir.
        path_logical, path_physical = self.get_document_path(docid)

        # The supplied filename does not exist at the supplied directory.
        if not os.path.exists('%s%s' % (path_physical, docid)):
            # Create the file with the supplied filename.
            fhandle = open('%s%s' % (path_physical, docid), 'w')
            fhandle.close()
            return True
        # The supplied filename does exist at the supplied directory.
        else:
            return False

    def get_document_path(self, docid):
        # Get the information for the supplied document.
        document = self.manage_DB.get_document_info(docid)

        # The supplied document exist.
        if document:
            # Get the information for the parent directory of the supplied
            # document.
            res = self.manage_DB.get_directory_info(
                document.info['parent_dir'])

            path_logical = ''
            path_physical = ''
            # While the parent_dir exist. The parent of the root directory
            # does not exist.
            while res:
                # Add the name/id of the parent directory to the path.
                path_logical = '%s/%s' % (res['name'], path)
                path_physical = '%s/%s' % (res['id'], path)
                # Get the information for the parent directory.
                res = self.manage_DB.get_directory_info(res['parent_dir'])

            return path_logical, path_physical
        # The supplied document does not exist.
        else:
            return '', ''

    def get_directory_documents(self, parent_dir):
        # Query for all the documents in the supplied directory.
        self.c.execute("""select * from document where parent_dir=?""",
            (parent_dir,))

        res = []
        for row in self.c:
            res.append({'id': row[0], 'name': row[1], 'parent_dir': row[2],
            'owner': row[3], 'infraction': row[4], 'last_mod_user': row[5],
            'last_mod_time': row[6], 'size': row[7]})

        return res

if __name__ == '__main__':
    doc = Document(0)
    doc.insert_invitation(0, 0, 'Join Sucka!')
    doc.insert_comment(0, 'I a comment Sucka!')
    doc.insert_complaint(0, 'I haz complaints Sucka!')

    docM = DocumentManager()
    docM.add_document('docname.txt', 1, 0, 1000)

    u = user.User(0)


    print 'Invitations:', u.view_invitations_to()[0]
    print '\nComments:', doc.view_comments()
    print '\nComplaints:', doc.view_complaints()
    print '\nAll Documents:', docM.get_all_documents()
    print '\nDir Documents:', docM.get_dir_documents(1)
