from manage import Manager
from sqlite3 import connect
import os
import re
from datetime import datetime


class Document:
    BASE_DIR = "dbs"

    def __init__(self, ID):
        self.manage = Manager()
        self.manage_DB = self.manage.manage_DB
        self.manage_Docs = self.manage.manage_Docs

        self.conn = connect(self.BASE_DIR + '/document.db')
        self.c = self.conn.cursor()

        self.info = self.manage_DB.get_info('document', rowid=ID)

        # Get the local and physical file system path for the document.
        path_logical, path_physical = self.manage_Docs.get_document_path(
            self.info['id'])
        self.info['lpath'] = path_logical
        self.info['ppath'] = path_physical
        return

    def init_autocompleteDB(self):
        # Create a newe copy of the autocomplete database.
        f = open(self.BASE_DIR + '/autocomplete.db', 'w')
        f.close()

        # Create a connection to the autocomplete database.
        conn = connect(self.BASE_DIR + '/autocomplete.db')
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
        conn = connect(self.BASE_DIR + '/autocomplete.db')
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
        conn = connect(self.BASE_DIR + '/autocomplete.db')
        # Create a cursor to the autocomplete database.
        c = conn.cursor()

        # Search for the query fragment and get only 1 result order ascending.
        c.execute("""select word from autocomplete where
            word Like ? and word != ?
            order by word asc
            limit 1""",
            (fragment + '%', fragment))

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

if __name__ == '__main__':
#    doc = Document(0)
#    doc.insert_invitation(0, 0, 'Join Sucka!')
#    doc.insert_comment(0, 'I a comment Sucka!')
#    doc.insert_complaint(0, 'I haz complaints Sucka!')
	print 'put stuff'
    #~ manage_Docs = DocumentManager(DBManager())
    #~ manage_Docs.create_autocompleteDB(1, "Hello World!")
#    docM.add_document('docname.txt', 1, 0, 1000)

#    u = user.User(0)


#    print 'Invitations:', u.view_invitations_to()[0]
#    print '\nComments:', doc.view_comments()
#    print '\nComplaints:', doc.view_complaints()
#    print '\nAll Documents:', docM.get_all_documents()
#    print '\nDir Documents:', docM.get_dir_documents(1)
