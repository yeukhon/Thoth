from sqlite3 import connect
from user import User
from datetime import datetime


class ApplicationManager:

    def __init__(self, user):
        self.user = user
        return

    def view_applications_pending(self):
        self.user.manage_User.c.execute("""select * from application
            where status=?""", (0,))

        res = []
        for row in self.user.manage_User.c:
            res.append({'id': row[0], 'username': row[1], 'password': row[2],
            'email': row[3], 'usergroup': row[4], 'content': row[5],
            'time': datetime.fromtimestamp(int(row[6])), 'status': row[7]})

        return res

if __name__ == "__main__":
    am = ApplicationManager(User(2))
    print am.view_applications_pending()
