from manage import Manager
from datetime import datetime


class User(object):

    def __init__(self, userid=0, username=''):
        # Initialize an instance of the Manager class for this user.
        self.manage = Manager()

        # Retrive the information for the current user based on the supplied
        # userid or username.
        self.update_user(userid=userid, username=username)

        return

    def update_user(self, userid=0, username=''):
        # If the userid was supplied:
        if userid:
            # Search for the user information by userid.
            self.info = self.manage.get_info('user', rowid=userid)
        # Else if the username was supplied:
        elif username:
            # Search for the user information by username.
            self.info = self.manage.get_info('user', where={
                'username': username})
        # Else neither the userid nor the username was supplied:
        else:
            # Default user, Guest.
            self.info = self.manage.get_info('user', rowid=1)

        # Set the information of the current user for the manager to be the
        # information that was just found. 
        self.manage.update_user_info(self.info)
        return

class RegularUser(User):

    def __init__(self, userid=0, username=''):
        # Initialize the user information and the Manager instance based on
        # the parent class, User.
        super(RegularUser, self).__init__(userid=userid, username=username)
        return

if __name__ == "__main__":
    ru = RegularUser(3)
    print ru.info
