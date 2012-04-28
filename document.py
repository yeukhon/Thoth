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

    def init_autocompleteDB(self):
        # Create a newe copy of the autocomplete database.
        f = open(self.BASE_DIR+'/autocomplete.db', 'w')
        f.close()

        # Create a connection to the autocomplete database.
        conn = connect(self.BASE_DIR+'/autocomplete.db')
        # Create a cursor to the autocomplete database.
        c = conn.cursor()

        # Create the autocomplete table.
        c.execute("""create table autocomplete (
            id integer primary key autoincrement,
            word text)""")

        # Open the document for reading.
        fhandle = open('%s%s' % (self.info['ppath'], self.info['id']), 'r')

        # Get the contents of the supplied document and force the contents to
        # lowercase.
        content = fhandle.read().lower()

        # Find all the words in the supplied content.
        words = re.findall('\w+', content)

        for word in words:
            # Only words with a length greater than 3 character will be used
            # as suggestions.
            if len(word) > 3:
                # Insert the word into the autocomplete table.
                conn.execute("""insert into autocomplete values (
                    NULL, ?)""", (word,))

        # Commit the changes to the autocomplete database.
        conn.commit()
        # Close the connection to the autocomplete database.
        conn.close()
        return

    def insert_word_autocompleteDB(self, word):
        # Create a connection to the autocomplete database.
        conn = connect(self.BASE_DIR+'/autocomplete.db')
        # Create a cursor to the autocomplete database.
        c = conn.cursor()

        # Search for the word.
        c.execute("""select * from autocomplete where
            word=?""",
            (word,))

        # Get 1 result.
        res = c.fetchone()

        # The result does not exist.
        if not res:
            c.execute("""insert into autocomplete values(
                NULL, ?)""", (word,))

            # Commit the changes to the autocomplete database.
            conn.commit()

        # Close the connection to the autocomplete database.
        conn.close()
        return

    def suggest_word_autocompleteDB(self, fragment):
         # Create a connection to the autocomplete database.
        conn = connect(self.BASE_DIR+'/autocomplete.db')
        # Create a cursor to the autocomplete database.
        c = conn.cursor()

        # Search for the query fragment and get only 1 result order ascending.
        c.execute("""select word from autocomplete where
            word Like ? and word != ?
            order by word asc
            limit 1""",
            (fragment+'%', fragment))

        # Get 1 result.
        res = c.fetchone()

        # Close the connection to the autocomplete database.
        conn.close()

        # The result exist.
        if res:
            return res[0]
        # The result does not exist.
        else:
            return ''


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

        # Return comments as a list.
        res = []
        for row in self.c:
            # Create a dictionary with the results and add the dictionary to
            # the list.
            res.append({'id': row[0], 'name': row[1], 'parent_dir': row[2],
                'owner': row[3], 'infraction': row[4],
                'last_mod_user': row[5], 'last_mod_time': row[6],
                'size': row[7]})

        # Return the list of results.
        return res

    def get_document_comments(self, docid):
        # Query for all comments for the supplied document.
        self.c.execute("""select * from comment where docid=?""",
            (docid, ))

        # Return comments as a list.
        res = []
        for row in self.c:
            # Create a dictionary with the results and add the dictionary to
            # the list.
            res.append({'id': row[0], 'docid': row[1], 'userid': row[2],
                'content': row[3], 'time': row[4]})

        # Return the list of results.
        return res

    def get_document_complaints(self, docid):
        # Query for all complaints for the supplied document.
        self.c.execute("""select * from complaint where docid=?""",
            (docid, ))

        # Return comments as a list.
        res = []
        for row in self.c:
            # Create a dictionary with the results and add the dictionary to
            # the list.
            res.append({'id': row[0], 'docid': row[1], 'userid': row[2],
                'content': row[3], 'time': row[4]})

        # Return the list of results.
        return res

    def is_member(self, docid, userid):
        # The supplied user is the owner of the supplied document.
        res = self.manage_DB.get_document_info(docid)
        if res['owner'] == userid:
            return True

        # Search for a member entry with the supplied user for the supplied
        # document.
        res = self.manage_DB.get_member_info(userid=userid, docid=docid)

        # There exist a member entry for the supplied user.
        if res:
            return True
        # There does not exist a member entry for the supplied user.
        else:
            return False

    def index_document(self, docid):
        # Get the local file system path for the supplied document.
        path_logical, path_physical = self.get_document_path(docid)

        # Open the document for reading.
        fhandle = open('%s%s' % (path_physical, docid), 'r')
        # Create an instance of the Porter Stemmer.
        PS = PorterStemmer()

        # Get the 1st line of the supplied document and force the contents to
        # lowercase.
        content = fhandle.readline().lower()

        # The text widget starts indexing its lines at 1, but columns start
        # indexing at 0.
        line_count = 1

        # While the supplied document has content to be read.
        while content != '':
            # Find all words from the current line of the supplied document
            # and put them in a list.
            words = re.findall('\w+', content)

            # For each word in the list of words from the current line.
            for word in words:
                # Only words whose length is greater than 3 will be indexed.
                if len(word) > 3:
                    # The column of the current word is its index in the
                    # current line.
                    col_count = content.find(word) + 1
                    # Using the PorterStemmer, find the root of the current
                    # word. Add the root word, with the current line and
                    # column number to the index.
                    self.manage_Indx.add_index_word(
                        PS.stem(word, 0, len(word)-1),
                        self.info['id'],
                        line_count,
                        col_count,
                        word)

            # Get the next line of the supplied document and force the
            # contents to lowercase.
            content = fhandle.readline().lower()
            # Increment the line count.
            line_count += 1

        # Close the supplied document file.
        fhandle.close()
        return

if __name__ == '__main__':
#    doc = Document(0)
#    doc.insert_invitation(0, 0, 'Join Sucka!')
#    doc.insert_comment(0, 'I a comment Sucka!')
#    doc.insert_complaint(0, 'I haz complaints Sucka!')

    manage_Docs = DocumentManager(DBManager())
    manage_Docs.create_autocompleteDB(1, "Hello World!")
#    docM.add_document('docname.txt', 1, 0, 1000)

#    u = user.User(0)


#    print 'Invitations:', u.view_invitations_to()[0]
#    print '\nComments:', doc.view_comments()
#    print '\nComplaints:', doc.view_complaints()
#    print '\nAll Documents:', docM.get_all_documents()
#    print '\nDir Documents:', docM.get_dir_documents(1)
