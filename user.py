from database import DBManager
from document import DocumentManager
from directory import DirectoryManager
from sqlite3 import connect
from datetime import datetime
from md5 import new


class User:
    BASE_DIR = "dbs"

    def __init__(self, userid=0, username=''):
        self.manage_DB = DBManager()
        self.manage_User = UserManager(self.manage_DB)
        self.manage_Docs = DocumentManager()
        self.manage_Dir = DirectoryManager()

        # Search for the user information by userid.
        if userid:
            self.info = self.manage_DB.get_user_info(userid=userid)
        # Search for the user information by username.
        elif username:
            self.info = self.manage_DB.get_user_info(username=username)
        # Default user, Guest.
        else:
            self.info = self.manage_DB.get_user_info(userid=1)
        return

    def update_user(self, userid):
        self.info = self.manage_DB.get_user_info(userid)
        return

    def view_invitations_to(self):
        self.manage_Docs.c.execute("""select * from invitation
            where userid_to=?""", (self.info['id'],))

        res = []
        for row in self.manage_Docs.c:
            doc_info = self.manage_DB.get_document_info(row[1])
            usr_info = self.manage_DB.get_user_info(row[2])
            if row[6] == 1: status = 'Accepted'
            elif row[6] == 0: status = 'Pending'
            else: status = 'Denied'

            res.append({'id': row[0], 'docid': doc_info['name'],
                'userid_from': usr_info['username'],
                'userid_to': self.info['username'], 'content': row[4],
                'time': datetime.fromtimestamp(int(row[5])), 'status': status})

        return res

    def view_invitations_from(self):
        self.manage_Docs.c.execute("""select * from invitation where userid_from=?""",
            (self.info['id'],))

        res = []
        for row in self.manage_Docs.c:
            doc_info = self.manage_DB.get_document_info(row[1])
            usr_info = self.manage_DB.get_user_info(row[3])
            if row[6] == 1: status = 'Accepted'
            elif row[6] == 0: status = 'Pending'
            else: status = 'Denied'

            res.append({'id': row[0], 'docid': doc_info['name'],
                'userid_from': self.info['username'],
                'userid_to': usr_info['username'], 'content': row[4],
                'time': datetime.fromtimestamp(int(row[5])), 'status': status})

        return res

class UserManager:
    BASE_DIR = "dbs"

    def __init__(self, dbm):
        self.manage_DB = dbm

        self.conn = connect(self.BASE_DIR+'/user.db')
        self.c = self.conn.cursor()
        return

    def close(self):
        self.c.close()
        return

if __name__ == "__main__":
    lg = UserManager()
#    lg.init_user()
#    lg.get_all_user()
#    lg.add_user("pent", "abc", "111@iii.com", 2)
#    lg.get_all_user()
#    lg.get_all_usergroup()
#    print '\nAdmin ID: ', lg.get_user_id('admin')
#    lg.close()
    u = User(0)
    print '\nInvitations: ', u.view_invitations_to()
