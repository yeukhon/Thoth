from database import Database
from porter import PorterStemmer
import os


class Manager(object):

    def __init__(self):
        # Intitialize the manager class.
        self.manage_DB = DBManager()
        
        # Initialize the manager for the users.
        self.manage_User = UserManager(self.manage_DB)
        # Initialize the manager for the documents.
        # Initialize the manager for the directories.
        self.manage_Docs = DocumentManager(self.manage_DB)
        self.manage_Dirs = DirectoryManager()
        # Initialize the manager for the index.
        self.manage_Indx = IndexManager(self.manage_DB)

        return

class DBManager(Database):

    def __init__(self, user_info={}):
        # Call the constuctor of the Database class.
        super(DBManager, self).__init__()

        # If the user information was supplied:
        if user_info:
            # Set the current user information to the supplied user.
            self.user_info = user_info
        # Else the user information was not supplied:
        else:
            # Initialize the current user information to be the guest user.
            self.user_info = super(DBManager, self).get_info('user', rowid=1)
        return

    def update_user_info(self, info):
        # Set the current user information to the supplier information.
        self.user_info = info
        return

    def insert_info(self, table, insert={}, verbose=False):
        # If the user has permission to preform the supplied action:
        res = super(DBManager, self).insert_info(
            table, insert=insert, verbose=verbose)
        # Else the user does not have persmission to preform the supplied action.
        return res

    def get_info(self, table, rowid=0, where={}, verbose=False):
        # If the user has permission to preform the supplied action:
        res = super(DBManager, self).get_info(
            table, rowid=rowid, where=where, verbose=verbose)
        # Else the user does not have persmission to preform the supplied action.
        return res

    def update_info(self, table, update={}, where={}, verbose=False):
        # If the user has permission to preform the supplied action:
        res = super(DBManager, self).update_info(
            table, update=update, where=where, verbose=verbose)
        # Else the user does not have persmission to preform the supplied action.
        return res
    
    def check_rights(self, table, action):
        # Check whether the current user has permission to preform the supplied
        # action on the supplied table.
        return

class UserManager:

    def __init__(self, dbm):
        # Save a instance of the supplied Manager class for later user.
        self.manage_DB = dbm
        return

    def get_invitations_to(self, userid):
        # Query for all invitations to the supplied user.
        rows = self.manage_DB.get_info('invitation', where={
            'userid_to': userid})

        # Get the information for the supplied user.
        usr_to = self.manage_DB.get_info('user', rowid=userid)

        # Initialize the list that will hold the results.
        res = []
        for row in rows:
            # Get the information for the document the current invitation is
            # referencing to.
            doc_info = self.manage_DB.get_info('document', rowid=row['docid'])
            # Get the information for the user of the current invitation.
            usr_from = self.manage_DB.get_info('user', rowid=row['userid_from'])

            # Determine the state of the invitation.
            if row['status'] == 1:
                status = 'Accepted'
            elif row['status'] == 0:
                status = 'Pending'
            else:
                status = 'Denied'

            # Create a dictionary with the results and add the dictionary to
            # the list.
            res.append({'id': row['id'], 'docid': doc_info['name'],
                'userid_from': usr_from['username'],
                'userid_to': usr_to['username'], 'content': row['content'],
                'time': datetime.fromtimestamp(int(row['time'])), 'status': status})

        # Return the list of results.
        return res

    def get_invitations_from(self, userid):
        # Query for all invitations to the supplied user.
        rows = self.manage_DB_Docs.get_invitation_info(where={'userid_from': userid})

        # Get the information for the supplied user.
        usr_from = self.manage_DB.get_user_info(userid=userid)

        res = []
        for row in rows:
            # Get the information for the document the current invitation is
            # referencing to.
            doc_info = self.manage_DB.get_document_info(row['docid'])
            # Get the information for the user of the current invitation.
            usr_to = self.manage_DB.get_user_info(row['userid_from'])

            # Determine the state of the invitation.
            if row['status'] == 1:
                status = 'Accepted'
            elif row['status'] == 0:
                status = 'Pending'
            else:
                status = 'Denied'

            # Create a dictionary with the results and add the dictionary to
            # the list.
            res.append({'id': row['id'], 'docid': doc_info['name'],
                'userid_from': usr_from['username'],
                'userid_to': usr_to['username'], 'content': row['content'],
                'time': datetime.fromtimestamp(int(row['time'])), 'status': status})

        # Return the list of results.
        return res

class DocumentManager:
    BASE_DIR = "dbs"

    def __init__(self, dbm):
        # Save an instance of the database manager.
        self.manage_DB = dbm
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
        document = self.manage_DB.get_info('document', rowid=docid)

        # The supplied document exist.
        if document:
            # Get the information for the parent directory of the supplied
            # document.
            res = self.manage_DB.get_info('directory',
                rowid=document['parent_dir'])

            path_logical = ''
            path_physical = ''
            # While the parent_dir exist. The parent of the root directory
            # does not exist.
            while res:
                # Add the name/id of the parent directory to the path.
                path_logical = '%s/%s' % (res['name'], path_logical)
                path_physical = '%s/%s' % (res['id'], path_physical)
                # Get the information for the parent directory.
                res = self.manage_DB.get_info('directory',
                    rowid=res['parent_dir'])

            return path_logical, path_physical
        # The supplied document does not exist.
        else:
            return '', ''

    def get_directory_documents(self, parent_dir):
        # Query for all the documents in the supplied directory.
        rows = self.manage_DB.get_info('document', where={
            'parent_dir': parent_dir})

        # Get the information for the supplied parent directory.
        dir_info = self.manage_DB.get_info('directory', rowid=parent_dir)

        # Return comments as a list.
        res = []
        for row in rows:
            # Get the information for the owner of the document.
            usr_info = self.manage_DB.get_info('user', rowid=row['owner'])
            # get the information of the last mod user.
            mod_info = self.manage_DB.get_info('user',
                rowid=row['last_mod_user'])

            # Create a dictionary with the results and add the dictionary to
            # the list.
            res.append({'id': row['id'], 'name': row['name'],
                'parent_dir': dir_info['name'], 'owner': usr_info['username'],
                'infraction': row['infraction'],
                'mod_user': mod_info['username'],
                'mod_time': datetime.fromtimestamp(int(row['last_mod_time'])),
                'size': row['size']})

        # Return the list of results.
        return res

    def get_document_comments(self, docid):
        # Query for all comments for the supplied document.
        rows = self.manage_DB.get_info('comment', where={'docid': docid})

        # Get the information for the supplied document.
        doc_info = self.manage_DB.get_info('document', rowid=docid)

        # Return comments as a list.
        res = []
        for row in rows:
            # Get the information for the user that wrote the comment.
            usr_info = self.manage_DB.get_info('user', rowid=row['userid'])

            # Create a dictionary with the results and add the dictionary to
            # the list.
            res.append({'id': row['id'], 'doc': doc_info['name'],
                'user': usr_info['username'], 'content': row['content'],
                'time': datetime.fromtimestamp(int(row['time']))})

        # Return the list of results.
        return res

    def get_document_complaints(self, docid):
        # Query for all complaints for the supplied document.
        rows = self.manage_DB.get_info('complaint', where={'docid': docid})

        # Get the information for the supplied document.
        doc_info = self.manage_DB.get_info('document', rowid=docid)

        # Return comments as a list.
        res = []
        for row in rows:
            # Get the information for the user that wrote the comment.
            usr_info = self.manage_DB.get_info('user', rowid=row['userid'])

            # Create a dictionary with the results and add the dictionary to
            # the list.
            res.append({'id': row['id'], 'doc': doc_info['name'],
                'user': usr_info['username'], 'content': row['content'],
                'time': datetime.fromtimestamp(int(row['time']))})

        # Return the list of results.
        return res

    def is_member(self, docid, userid):
        # The supplied user is the owner of the supplied document.
        res = self.manage_DB.get_info('document', rowid=docid)
        if res['owner'] == userid:
            return True

        # Search for a member entry with the supplied user for the supplied
        # document.
        res = self.manage_DB.get_info('member', where={
            'userid': userid, 'docid': docid})

        # There exist a member entry for the supplied user.
        if res:
            return True
        # There does not exist a member entry for the supplied user.
        else:
            return False

class DirectoryManager:
    BASE_DIR = "dbs"

    def __init__(self):
        self.manage_DB = DBManager()
        return

    def get_directory_path(self, directoryid):
        # Get the information for the supplied directory.
        res = self.manage_DB.get_info('directory', rowid=directoryid)

        path_logical = ''
        path_physical = ''
        # While the parent_dir exist. The parent of the root directory
        # does not exist.
        while res:
            # Add the name/id of the parent directory to the path.
            path_logical = '%s/%s' % (res['name'], path_logical)
            path_physical = '%s/%s' % (res['id'], path_physical)
            # Get the information for the parent directory.
            res = self.manage_DB.get_info('directory', rowid=res['parent_dir'])

        return path_logical, path_physical

    def create_directory(self, directoryid):
        # Get the local file system path for the supplied directory.
        path_logical, path_physical = self.get_directory_path(directoryid)

        # The supplied folder name does not exist at the supplied directory.
        if not os.path.isdir('%s' % path_physical):
            # Create the folder with the supplied folder name.
            os.mkdir('%s' % path_physical)
            return True
        # The supplied folder name does exist at the supplied directory.
        else:
            return False

    def get_directory_directories(self, directoryid):
        # Query for all the directories in the supplied directory.
        res = self.manage_DB.get_info('directory', where={
            'parent_dir': directoryid})

        for row in res:
            # Create a dictionary with the results and add the dictionary to
            # the list.
            row['parent'] = self.manage_DB.get_info(
                'directory', rowid=row['parent_dir'])['name']

        # Return the list of results.
        return res

class IndexManager:
    BASE_DIR = "dbs"

    def __init__(self, dbm):
        self.manage_DB = dbm
        return

    def add_index_word(self, root, docid, line, column, branch_word):
        # Search for the root word in the index word table.
        res = self.manage_DB.get_info('index_word', where={'word': root})

        # The root word does not exist in the table.
        if not res:
            # Insert the root word into the index_word table.
            self.manage_DB.insert_info('index_word', insert={'word': root})
            # Get the id of the newly inserted root word.
            wordid = self.manage_DB.get_info('index_word', where={
                'word': root})[0]['id']
        # The root word does exist in the table.
        else:
            # Get the id of the root word.
            wordid = res[0]['id']

        # Search for a reference with the supplied information.
        res = self.manage_DB.get_info('index_ref', where={
            'wordid': wordid, 'docid': docid, 'line': line, 'column': column})

        # A reference with the supplied information does not already exist.
        if not res:
            # Insert a reference with the supplied information and return the
            # the result of the insertion.
            return self.manage_DB.insert_info('index_ref', where={
                'wordid': wordid, 'docid': docid, 'line': line,
                'column': column, 'branch_word': branch_word})
        # A reference with the supplied information already exist, so return
        # False.
        else:
            return False

    def search(self, word):
        # Create an instance of the Porter Stemmer.
        PS = PorterStemmer()

        # Get the information for the supplied word.
        res = self.manage_DB.get_info('index_word', where={
            'word': PS.stem(word, 0, len(word) - 1)})

        # The supplied word exist in the index_word table.
        if res:
            # Extract the id for the supplied word.
            wordid = res['id']

            # Get all the entries in the index reference database that refer to
            # the supplied wordid.
            res = self.manage_DB.get_info('index_ref', where={
                'wordid': wordid})
                
            # For ever entry in the list.
            for row in res:
                # Modify the current row to contain the stem word.
                row['word'] =  self.manage_DB.get_info(
                    'index_word', rowid=row[1])['word']
                # Modify the current row to contain the document name. 
                row['doc'] = self.manage_DB.get_info(
                    'document', rowid=row[2])['name']

            # Return the list of all the results.
            return res
        # The supplied word does not exist in the index_word table, so return
        # and empty list.
        else:
            return []

    def index_document(self, docid, path_physical):
        # Get the information for the supplied document.
        document = self.manage_DB.get_info('document', rowid=docid)
        
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
                        PS.stem(word, 0, len(word) - 1),
                        docid,
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

if __name__ == "__main__":
    m = Manager()
    print m.manage_DB.user_info
