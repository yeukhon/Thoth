from database import DBManager
from document import DocumentManager
from directory import DirectoryManager
from sqlite3 import connect
from datetime import datetime
from md5 import new


class User:
    BASE_DIR = "dbs"

    def __init__(self, userid):
        self.manage_DB = DBManager()
        self.manage_User = UserManager()
        self.manage_Docs = DocumentManager()
        self.manage_Dir = DirectoryManager()

        self.info = self.manage_DB.get_user_info(userid)
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

    def __init__(self):
        self.init_DBM = DBManager()

        self.conn = connect(self.BASE_DIR+'/user.db')
        self.c = self.conn.cursor()
        return

    def get_all_user(self):
        self.c.execute("""select * from user""")
        for row in self.c:
            print row
        return

    def get_all_usergroup(self):
        self.c.execute("""select * from usergroup""")
        for row in self.c:
            print row
        return

    def get_user_id(self, name):
        self.c.execute("""select id from user where lower(username)=?""", (name.lower(),))
        res = self.c.fetchone()

        if res != None:
            return True, res[0]
        else:
            return False,

    def get_usergroup_id(self, name):
        self.c.execute("""select id from usergroup where name=?""", (name,))
        res = self.c.fetchone()

        if res != None:
            return True, res[0]
        else:
            return False,

    def add_user(self, username, password, email, group):
        userid = self.get_user_id(username)
        if userid[0]:
            return False, userid[1]

        t = (username, new(password).hexdigest(), email, group)
        self.c.execute("""insert into user values (NULL, ?, ?, ?, ?, 0)""", t)

        self.conn.commit()
        return self.get_user_id(username)

    def add_usergroup(self, name):
        self.c.execute("""select id from usergroup where
            name=? """, (name,))
        res = self.c.fetchone()

        if res != None:
            return False, res[0]

        t = (name, )
        self.c.execute("""insert into usergroup values (NULL, ?)""", t)
        self.conn.commit()
        return self.get_usergroup_id(name)

    def user_in_DB(self, username, password):
        t = (username, new(password).hexdigest())
        self.c.execute("""select id from user where
            lower(username)=? and password=?""",
            t)
        res = self.c.fetchall()
        if len(res) == 1:
            return True, res[0][0]
        else:
            return False, 0

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
