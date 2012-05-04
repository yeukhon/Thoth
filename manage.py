from database import DBManager


class Manager(object):

    def __init__(self, user=None):
        # Initialize the manager for the databases.
        self.manage_DB = DBManager()
        # Initialize the manager for the documents.
        self.manage_Docs = DocumentManager()
        # Initialize the manager for the users.
        self.manage_User = UserManager()
        # Initialize the manager for the directories.
        self.manage_Dirs = DirectoryManager()

        # Initialize the current user of this manager to the supplied user.
        self.user = user
        return

    def update_user(self,


if __name__ == "__main__":
    m = Manager()
