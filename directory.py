from database import DBManager
from sqlite3 import connect
import os


class DirectoryManager:
    BASE_DIR = "dbs"

    def __init__(self):
        self.manage_DB = DBManager()

        self.conn = connect(self.BASE_DIR + '/document.db')
        self.c = self.conn.cursor()
        return

    def get_directory_path(self, directoryid):
        # Get the information for the supplied directory.
        res = self.manage_DB.get_directory_info(directoryid)

        path_logical = ''
        path_physical = ''
        # While the parent_dir exist. The parent of the root directory
        # does not exist.
        while res:
            # Add the name/id of the parent directory to the path.
            path_logical = '%s/%s' % (res['name'], path_logical)
            path_physical = '%s/%s' % (res['id'], path_physical)
            # Get the information for the parent directory.
            res = self.manage_DB.get_directory_info(res['parent_dir'])

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
        self.c.execute("""select * from directory where parent_dir=?""",
            (directoryid,))

        # Return directories as a list.
        res = []
        for row in self.c:
            # Create a dictionary with the results and add the dictionary to
            # the list.
            res.append({'id': row[0], 'name': row[1], 'parent_dir': row[2]})

        # Return the list of results.
        return res
