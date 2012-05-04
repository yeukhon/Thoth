from database import DBManager
from directory import DirectoryManager
from sqlite3 import connect
from datetime import datetime


class User(object):
    BASE_DIR = "dbs"

    def __init__(self, userid=0, username=''):
        self.manage_DB = DBManager()
        self.manage_User = UserManager(self.manage_DB)
        self.manage_Dir = DirectoryManager()

        # Search for the user information by userid.
        if userid:
            self.info = self.manage_DB.get_info('user', rowid=userid)
        # Search for the user information by username.
        elif username:
            self.info = self.manage_DB.get_info('user', where={
                'username': username})
        # Default user, Guest.
        else:
            self.info = self.manage_DB.get_info('user', rowid=1)
        return

    def update_user(self, userid):
        self.info = self.manage_DB.get_info('user', rowid=userid)
        return

class RegularUser(User):
    BASE_DIR = "dbs"

    def __init__(self, userid=0, username=''):
        super(RegularUser, self).__init__(userid=userid, username=username)
        return


class UserManager:
    BASE_DIR = "dbs"

    def __init__(self, dbm):
        self.manage_DB = dbm

        self.conn = connect(self.BASE_DIR + '/user.db')
        self.c = self.conn.cursor()
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
        rows = self.manage_Docs.get_invitation_info(where={'userid_from': userid})

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


if __name__ == "__main__":
    um = UserManager(DBManager())
    ash = RegularUser(2)
    print ash.info
