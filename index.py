from database import DBManager
from sqlite3 import connect
from porter import PorterStemmer


class IndexManager:
    BASE_DIR = "dbs"

    def __init__(self):
        self.manage_DB = DBManager()

        self.conn = connect(self.BASE_DIR+'/index.db')
        self.c = self.conn.cursor()
        return

    def add_index_word(self, root, docid, line, column, branch_word):
        # Search for the root word in the index word table.
        res = self.manage_DB.get_index_word_info(word=root)

        # The root word does not exist in the table.
        if not res:
            # Insert the root word into the index_word table.
            self.manage_DB.insert_index_word(root)
            # Get the id of the newly inserted root word.
            wordid = self.manage_DB.get_index_word_info(word=root)['id']
        # The root word does exist in the table.
        else:
            # Get the id of the root word.
            wordid = res['id']

        # Search for a reference with the supplied information.
        res = self.manage_DB.get_index_ref_info(
            wordid=wordid, docid=docid, line=line, column=column)

        # A reference with the supplied information does not already exist.
        if not res:
            # Insert a reference with the supplied information and return the
            # the result of the insertion.
            return self.manage_DB.insert_index_ref(
                wordid, docid, line, column, branch_word)
        # A reference with the supplied information already exist, so return
        # False.
        else:
            return False

    def search(self, word):
        # Create an instance of the Porter Stemmer.
        PS = PorterStemmer()

        # Get the information for the supplied word.
        res = self.manage_DB.get_index_word_info(
            PS.stem(word, 0, len(word)-1))

        # The supplied word exist in the index_word table.
        if res:
            # Extract the id for the supplied word.
            wordid = res['id']

            # Return the found entries as a list.
            res = []

            # Query the index_ref table for all the entries whose wordid
            # match the supplied word's id.
            self.c.execute("""select * from index_ref where wordid=?""",
                (wordid,))

            # Retrieve all the results of the query as a list.
            entries = self.c.fetchall()

            # For ever entry in the list.
            for row in entries:
                # Create a dictionary with the results and add the dictionary
                # to the list.
                res.append({
                    'id': row[0],
                    'word': self.manage_DB.get_index_word_info(row[1])['word'],
                    'docid': row[2],
                    'doc': self.manage_DB.get_document_info(row[2])['name'],
                    'line': row[3], 'column': row[4],
                    'branch_word': row[5]})

            # Return the list of all the results.
            return res
        # The supplied word does not exist in the index_word table, so return
        # and empty list.
        else:
            return []
