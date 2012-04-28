import os
from sqlite3 import connect
from time import time
from md5 import new


class DBManager():
    BASE_DIR = "dbs"
    DOCS_DIR = "1"

    def __init__(self):
        self.check()

        return

    def check(self):
        # First we must check whether the directory where the databases are
        # kept exists, if it does not, then we create just the directory.
        if not os.path.isdir(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)

        # Check whether the user database exist, if it does not, then create
        # it and add the necessary tables and deflaut values.
        self.check_create_userDB()
        # Check whether the document database exist, if it does not, then
        # create it and add the necessary tables and deflaut values.
        self.check_create_documentDB()
        # Check whether the index database exist, if it does not, then
        # create it and add the necessary tables and deflaut values.
        self.check_create_indexDB()

        # Last we must check whether the directory where the documents are
        # kept exists, if it does not, then we create just the directory.
        if not os.path.isdir(self.DOCS_DIR):
            os.mkdir(self.DOCS_DIR)

        return

    def check_DB_exist(self, conn, name):
        """Checks whether a table with the specified name exist within the
        specified database.
        @param  conn    The connect to the database.
        @param  name    The name of the table.
        @return True    The table exist.
                False   The table does not exist within the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()
        # The query searches the database for a table with the specified name
        # and returns the number of occurences it finds.
        c.execute(
            """select count(*) from sqlite_master where name=?""",
            (name,))
        # We are only expecting one row from the query and only need the first
        # item from the row, i.e. the number of occurences. Note that if the
        # number of occurences is 1, then the conditional will be True.
        if c.fetchone()[0]:
            # The cursor cannot be closed before the conditional statement
            # because of the use of the "fetchone" method of the cursor.
            c.close()
            # The table is found in the database.
            return True
        else:
            # Close the cursor for this branch of the conditional.
            c.close()
            # The table is not found in the database.
            return False

    def check_create_userDB(self):
        """Checks whether the user database is where it is suppose to be and
        if it is not found, then it will create the file and add the tables"""
        # Check the base directory for the user database, if it is not found
        # then proceed with the conditional.
        if not os.path.exists(self.BASE_DIR + '/user.db'):
            # The database does not exist, so create the database file.
            f = open(self.BASE_DIR + '/user.db', 'w')
            # As of yet, we do not want to do anything to the database in this
            # file writing mode.
            f.close()

        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/user.db')

        # Check whether the application table does not exist in the database.
        if not self.check_DB_exist(conn, 'application'):
            # The application table does not exist, so create the table and
            # insert the default values.
            self.init_table_application(conn)

        # Check whether the user table does not exist in the database.
        if not self.check_DB_exist(conn, 'user'):
            # The user table does not exist, so create the table and insert
            # the default values.
            self.init_table_user(conn)

        # Check whether the usergroup table does not exist in the database.
        if not self.check_DB_exist(conn, 'usergroup'):
            # The usergroup table does not exist, so create the table and
            # insert the default values.
            self.init_table_usergroup(conn)

        # Check whether the invitation table does not exist in the database.
        if not self.check_DB_exist(conn, 'invitation'):
            # The invitation table does not exist, so create the table and
            # insert the default values.
            self.init_table_invitation(conn)

        # Close the connection to the database.
        conn.close()
        return

    def check_create_documentDB(self):
        """Checks whether the document database is where it is suppose to be
        and if it is not found, then it will create the file and add the
        tables."""
        # Check the base directory for the document database, if it is not
        # found then proceed with the conditional.
        if not os.path.exists(self.BASE_DIR + '/document.db'):
            # The database does not exist, so create the database file.
            f = open(self.BASE_DIR + '/document.db', 'w')
            # As of yet, we do not want to do anything to the database in this
            # file writing mode.
            f.close()

        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/document.db')

        # Check whether the document table does not exist in the database.
        if not self.check_DB_exist(conn, 'document'):
            # The document table does not exist, so create the table and
            # insert the default values.
            self.init_table_document(conn)

        # Check whether the comment table does not exist in the database.
        if not self.check_DB_exist(conn, 'comment'):
            # The comment table does not exist, so create the table and
            # insert the default values.
            self.init_table_comment(conn)

        # Check whether the complaint table does not exist in the database.
        if not self.check_DB_exist(conn, 'complaint'):
            # The complaint table does not exist, so create the table and
            # insert the default values.
            self.init_table_complaint(conn)

        # Check whether the directory table does not exist in the database.
        if not self.check_DB_exist(conn, 'directory'):
            # The directory table does not exist, so create the table and
            # insert the default values.
            self.init_table_directory(conn)

        # Check whether the member table does not exist in the database.
        if not self.check_DB_exist(conn, 'member'):
            # The member table does not exist, so create the table and insert
            # the default values.
            self.init_table_member(conn)

        # Close the connection to the database.
        conn.close()
        return

    def check_create_indexDB(self):
        """Checks whether the index database is where it is suppose to be and
        if it is not found, then it will create the file and add the tables"""
        # Check the base directory for the index database, if it is not found
        # then proceed with the conditional.
        if not os.path.exists(self.BASE_DIR + '/index.db'):
            # The database does not exist, so create the database file.
            f = open(self.BASE_DIR + '/index.db', 'w')
            # As of yet, we do not want to do anything to the database in this
            # file writing mode.
            f.close()

        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/index.db')

        # Check whether the user table does not exist in the database.
        if not self.check_DB_exist(conn, 'stop_words'):
            # The user table does not exist, so create the table and insert
            # the default values.
            self.init_table_stop_words(conn)

        # Check whether the user table does not exist in the database.
        if not self.check_DB_exist(conn, 'index_word'):
            # The user table does not exist, so create the table and insert
            # the default values.
            self.init_table_index_word(conn)

        # Check whether the user table does not exist in the database.
        if not self.check_DB_exist(conn, 'index_ref'):
            # The user table does not exist, so create the table and insert
            # the default values.
            self.init_table_index_ref(conn)

        # Close the connection to the database.
        conn.close()
        return

    def init_table_application(self, conn):
        """Create the application table in the user database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Create the application table with the appropriate fields.
        c.execute("""create table application (
            id integer primary key autoincrement,
            username text,
            password text,
            email text,
            usergroup integer,
            content text,
            time real,
            status integer)""")

        # Insert a default user application, in the Ordinary User usergroup.
        c.execute("""insert into application values (
            NULL,
            'OU',
            ?,
            'fake@domain.com',
            2,
            'I am a test user!',
            ?,
            0)""", (new('default').hexdigest(), time()))

        # Commit all the changes we have made to the application database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        return

    def get_application_info(self, appid=0, username=''):
        # At this point, the application database must exist, so create a
        # database connection to the file.
        conn = connect(self.BASE_DIR + '/user.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Search by userid.
        if appid:
            c.execute("""select * from application where id=?""", (appid,))
        # Search by username.
        elif username:
            c.execute("""select * from application where lower(username)=?""",
                (username.lower(),))

        # Get 1 result, if any exist.
        row = c.fetchone()

        if row:
            res = {'id': row[0], 'username': row[1], 'password': row[2],
                'email': row[3], 'usergroup': row[4], 'content': row[5],
                'time': row[6], 'status': row[7]}
        else:
            res = {}

        # Close the cursor that we created to the database and then close the
        # database itself.
        c.close()
        conn.close()
        return res

    def insert_application(
        self, username, password, email, usergroup, content, time, status):
        # There does not already exist an application in the database from
        # this user.
        if not self.get_application_info(username=username):
            # At this point, the application database must exist, so create a
            # database connection to the file.
            conn = connect(self.BASE_DIR + '/user.db')

            # Create the cursor to preform the queries.
            c = conn.cursor()

            c.execute("""insert into application values (
                NULL, ?, ?, ?, ?, ?, ?, ?)""",
                (username, password, email, usergroup, content, time, status))

            # Commit all the changes we have made to the application database.
            conn.commit()

            # Close the cursor that we created to the database and then close
            # the database itself.
            c.close()
            conn.close()
            return True
        # There already exist an application in the database from this user.
        else:
            return False

    def init_table_user(self, conn):
        """Create the user table in the user database and insert the default
        values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Create the user table with the appropriate fields. The "id" field
        # denotes the user, not the username.
        c.execute("""create table user (
            id integer primary key autoincrement,
            username text,
            password text,
            email text,
            usergroup integer,
            infraction integer)""")

        # Insert a default user, Admin, in the Super User usergroup.
        c.execute("""insert into user values (
            NULL,
            'Guest',
            '000',
            'fake@domain.com',
            4,
            0)""")
        c.execute("""insert into user values (
            NULL,
            'admin',
            '123',
            'example@domain.com',
            1,
            0)""")
        c.execute("""insert into user values (
            NULL,
            'kevin',
            '123',
            'example@domain.com',
            2,
            0)""")

        # Commit all the changes we have made to the user database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        return

    def get_user_info(self, userid=0, username=''):
        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/user.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Search by userid.
        if userid:
            c.execute("""select * from user where id=?""", (userid,))
        # Search by username.
        elif username:
            c.execute("""select * from user where lower(username)=?""",
                (username.lower(),))

        # Get 1 result, if any exist.
        row = c.fetchone()

        if row:
            res = {'id': row[0], 'username': row[1], 'password': row[2],
            'email': row[3], 'usergroup': row[4], 'infraction': row[5]}
        else:
            res = {}

        # Close the cursor that we created to the database and then close the
        # database itself.
        c.close()
        conn.close()
        return res

    def insert_user(self, username, password, email, usergroup, infraction):
        # There does not already exist a user with the supplied username.
        if not self.get_user_info(username=username):
            # At this point, the user database must exist, so create a database
            # connection to the file.
            conn = connect(self.BASE_DIR + '/user.db')

            # Create the cursor to preform the queries.
            c = conn.cursor()

            c.execute("""insert into user values (
                NULL, ?, ?, ?, ?, ?)""",
                (username, password, email, usergroup, infraction))

            # Commit all the changes we have made to the application database.
            conn.commit()

            # Close the cursor that we created to the database and then close
            # the database itself.
            c.close()
            conn.close()
            return True
        # There already exist a user with the supplied username.
        else:
            return False

    def init_table_usergroup(self, conn):
        """Create the user table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Create the usergroup table with the appropriate fields. The "id"
        # field denotes the usergroup, not the name field.
        c.execute("""create table usergroup (
            id integer primary key autoincrement,
            name text)""")

        # Insert the default usergroups:
        c.execute("""insert into usergroup values (NULL,'Super')""")
        c.execute("""insert into usergroup values (NULL,'Normal')""")
        c.execute("""insert into usergroup values (NULL,'Suspended')""")
        c.execute("""insert into usergroup values (NULL,'Vistor')""")

        # Commit all the changes we have made to the user database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        return

    def get_usergroup_info(self, usergroupid=0, name=''):
        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/user.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Search by usergroupid.
        if usergroupid:
            c.execute("""select * from usergroup where id=?""",
                (usergroupid,))
        # Search by name.
        elif name:
            c.execute("""select * from usergroup where lower(name)=?""",
                (name.lower(),))

        # Get 1 result, if any exist.
        row = c.fetchone()

        if row:
            res = {'id': row[0], 'name': row[1]}
        else:
            res = {}

        # Close the cursor that we created to the database and then close the
        # database itself.
        c.close()
        conn.close()
        return res

    def insert_usergroup(self, name):
        # There does not already exist a usergroup with the supplied name.
        if not self.get_usergroup_info(name=name):
            # At this point, the user database must exist, so create a database
            # connection to the file.
            conn = connect(self.BASE_DIR + '/user.db')

            # Create the cursor to preform the queries.
            c = conn.cursor()

            c.execute("""insert into usergroup values (NULL, ?)""", (name,))

            # Commit all the changes we have made to the application database.
            conn.commit()

            # Close the cursor that we created to the database and then close
            # the database itself.
            c.close()
            conn.close()
            return True
        # There already exist a usergroup with the supplied name.
        else:
            return False

    def init_table_document(self, conn):
        """Create the document table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Create the document table with the appropriate fields. The "id"
        # field denotes the document, not the name field.
        c.execute("""create table document (
            id integer primary key autoincrement,
            name text,
            parent_dir integer,
            owner integer,
            infraction integer,
            last_mod_user integer,
            last_mod_time real,
            size integer
        )""")

        # Not necessary, but insert a test document.
        t = ('Test.txt', 0, 1, 0, 1, time(), 0)
        c.execute("""insert into document values (
            NULL,
            ?, ?, ?, ?, ?, ?, ? )""", t)

        # Commit all the changes we have made to the user database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        return

    def get_document_info(self, docid=0, name='', parent_dir=0):
        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/document.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Search by docid.
        if docid:
            c.execute("""select * from document where id=?""", (docid,))
        # Search by name and parent_dir.
        elif name and parent_dir:
            c.execute("""select * from document where
                lower(name)=? and parent_dir=?""", (name.lower(), parent_dir))

        # Get 1 result, if any exist.
        row = c.fetchone()

        if row:
            res = {'id': row[0], 'name': row[1], 'parent_dir': row[2],
                'owner': row[3], 'infraction': row[4], 'last_mod_user': row[5],
                'last_mod_time': row[6], 'size': row[7]}
        else:
            res = {}

        # Close the cursor that we created to the database and then close the
        # database itself.
        c.close()
        conn.close()
        return res

    def insert_document(
        self, name, parent_dir, owner, infraction, last_mod_user,
        last_mod_time, size):
        # There does not already exist a document in the supplied directory
        # with the supplied name.
        if not self.get_document_info(name=name, parent_dir=parent_dir):
            # At this point, the user database must exist, so create a database
            # connection to the file.
            conn = connect(self.BASE_DIR + '/document.db')

            # Create the cursor to preform the queries.
            c = conn.cursor()

            c.execute("""insert into document values (
                NULL, ?, ?, ?, ?, ?, ?, ? )""",
                (name, parent_dir, owner, infraction, last_mod_user,
                last_mod_time, size))

            # Commit all the changes we have made to the application database.
            conn.commit()

            # Close the cursor that we created to the database and then close
            # the database itself.
            c.close()
            conn.close()
            return True
        # There already exist a document in the supplied directory with the
        # supplied name.
        else:
            return False

    def init_table_comment(self, conn):
        """Create the comment table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Create the document table with the appropriate fields. The "id"
        # field denotes the document, not the name field.
        c.execute("""create table comment (
            id integer primary key autoincrement,
            docid integer,
            userid integer,
            content text,
            time real
        )""")

        # Not necessary, but insert a test comment.
        t = (0, 0, 'Sample content...', time())
        c.execute("""insert into comment values (
            NULL,
            ?, ?, ?, ? )""", t)

        # Commit all the changes we have made to the document database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        return

    def get_comment_info(self, commentid=0, docid=0, userid=0, content=''):
        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/document.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Search by commentid.
        if commentid:
            c.execute("""select * from comment where id=?""", (commentid,))
        # Search by docid and userid and content.
        elif docid and userid and content:
            c.execute("""select * from comment where
                docid=? and userid=? and lower(content)=?""",
                (docid, userid, content.lower()))

        # Get 1 result, if any exist.
        row = c.fetchone()

        if row:
            res = {'id': row[0], 'docid': row[1], 'userid': row[2],
                'content': row[3], 'time': row[4]}
        else:
            res = {}

        # Close the cursor that we created to the database and then close the
        # database itself.
        c.close()
        conn.close()
        return res

    def insert_comment(self, docid, userid, content, time):
        # There does not already exist a comment on the supplied document from
        # the supplied user with the supplied content.
        if not self.get_comment_info(
            docid=docid, userid=userid, content=content):
            # At this point, the user database must exist, so create a database
            # connection to the file.
            conn = connect(self.BASE_DIR + '/document.db')

            # Create the cursor to preform the queries.
            c = conn.cursor()

            c.execute("""insert into comment values
                (NULL, ?, ?, ?, ?)""",
                (docid, userid, content, time))

            # Commit all the changes we have made to the application database.
            conn.commit()

            # Close the cursor that we created to the database and then close
            # the database itself.
            c.close()
            conn.close()
            return True
        # There already exist a comment on the supplied document from the
        # supplied user with the supplied content.
        else:
            return False

    def init_table_invitation(self, conn):
        """Create the invitation table in the usergroup database and insert
        the default values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Create the invitation table with the appropriate fields. The "id"
        # field denotes the document, not the name field.
        c.execute("""create table invitation (
            id integer primary key autoincrement,
            docid integer,
            userid_from integer,
            userid_to integer,
            content text,
            time real,
            status integer
        )""")

        # Commit all the changes we have made to the document database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        return

    def get_invitation_info(self, invitationid=0,
        docid=0, userid_from=0, userid_to=0):
        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/user.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Search by invitationid.
        if invitationid:
            c.execute("""select * from invitation where id=?""",
                (invitationid,))
        # Search by docid and userid_from and userid_to.
        elif docid and userid_from and userid_to:
            c.execute("""select * from invitation where
                docid=? and userid_from=? and userid_to=?""",
                (docid, userid_from, userid_to))

        # Get 1 result, if any exist.
        row = c.fetchone()

        if row:
            res = {'id': row[0], 'docid': row[1], 'userid_from': row[2],
                'userid_to': row[3], 'content': row[4], 'time': row[5],
                'status': row[6]}
        else:
            res = {}

        # Close the cursor that we created to the database and then close the
        # database itself.
        c.close()
        conn.close()
        return res

    def insert_invitation(
        self, docid, userid_from, userid_to, content, time, status):
        # There does not already exist a invitation to the supplied document
        # from the supplied user to the supplied recipient.
        if not self.get_invitation_info(
            docid=docid, userid_from=userid_from, userid_to=userid_to):
            # At this point, the user database must exist, so create a database
            # connection to the file.
            conn = connect(self.BASE_DIR + '/user.db')

            # Create the cursor to preform the queries.
            c = conn.cursor()

            c.execute("""insert into invitation values
                (NULL, ?, ?, ?, ?, ?)""",
                (docid, userid_from, userid_to, content, time, status))

            # Commit all the changes we have made to the application database.
            conn.commit()

            # Close the cursor that we created to the database and then close
            # the database itself.
            c.close()
            conn.close()
            return True
        # There already exist a invitation to the supplied document from the
        # supplied user to the supplied recipient.
        else:
            return False

    def init_table_complaint(self, conn):
        """Create the complaint table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Create the complaint table with the appropriate fields. The "id"
        # field denotes the document, not the name field.
        c.execute("""create table complaint (
            id integer primary key autoincrement,
            docid integer,
            userid integer,
            content text,
            time real,
            status integer
        )""")

        # Not necessary, but insert a test complaint.
        t = (0, 0, 'Sample complaint...', time(), 0)
        c.execute("""insert into complaint values (
            NULL,
            ?, ?, ?, ?, ? )""", t)

        # Commit all the changes we have made to the document database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        return

    def get_complaint_info(self, complaintid=0, docid=0, userid=0):
        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/document.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Search by complaintid.
        if complaintid:
            c.execute("""select * from complaint where id=?""",
                (complaintid,))
        # Search by docid and userid.
        elif docid and userid:
            c.execute("""select * from complaint where
                docid=? and userid=?""",
                (docid, userid))

        # Get 1 result, if any exist.
        row = c.fetchone()

        if row:
            res = {'id': row[0], 'docid': row[1], 'userid': row[2],
                'content': row[3], 'time': row[4], 'status': row[5]}
        else:
            res = {}

        # Close the cursor that we created to the database and then close the
        # database itself.
        c.close()
        conn.close()
        return res

    def insert_complaint(self, docid, userid, content, time, status):
        # There does not already exist a complaint on the supplied document
        # from the supplied user.
        if not self.get_complaint_info(docid=docid, userid=userid):
            # At this point, the user database must exist, so create a database
            # connection to the file.
            conn = connect(self.BASE_DIR + '/document.db')

            # Create the cursor to preform the queries.
            c = conn.cursor()

            c.execute("""insert into complaint values
                (NULL, ?, ?, ?, ?, ?)""",
                (docid, userid, content, time, status))

            # Commit all the changes we have made to the application database.
            conn.commit()

            # Close the cursor that we created to the database and then close
            # the database itself.
            c.close()
            conn.close()
            return True
        # There already exist a complaint on the supplied document from the
        # supplied user.
        else:
            return False

    def init_table_member(self, conn):
        """Create the member table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Create the member table with the appropriate fields.
        c.execute("""create table member (
            id integer primary key autoincrement,
            userid integer,
            docid integer
        )""")

        # Commit all the changes we have made to the user database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        return

    def get_member_info(self, memberid=0, userid=0, docid=0):
        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/document.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Search by memberid.
        if memberid:
            c.execute("""select * from member where id=?""", (memberid,))
        # Search by docid and userid.
        elif userid and docid:
            c.execute("""select * from member where
                userid=? and docid=?""", (userid, docid))

        # Get 1 result, if any exist.
        row = c.fetchone()

        if row:
            res = {'id': row[0], 'userid': row[1], 'docid': row[2]}
        else:
            res = {}

        # Close the cursor that we created to the database and then close the
        # database itself.
        c.close()
        conn.close()
        return res

    def insert_member(self, userid, docid):
        # The supplied user is not already a member of the supplied document.
        if not self.get_member_info(userid=userid, docid=docid):
            # At this point, the user database must exist, so create a database
            # connection to the file.
            conn = connect(self.BASE_DIR + '/document.db')

            # Create the cursor to preform the queries.
            c = conn.cursor()

            c.execute("""insert into member values
                (NULL, ?, ?)""",
                (userid, docid))

            # Commit all the changes we have made to the application database.
            conn.commit()

            # Close the cursor that we created to the database and then close
            # the database itself.
            c.close()
            conn.close()
            return True
        # The supplied user is already a member of the supplied document.
        else:
            return False

    def init_table_directory(self, conn):
        """Create the directory table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Create the directory table with the appropriate fields. The "id"
        # field denotes the directory, not the name field.
        c.execute("""create table directory (
            id integer primary key autoincrement,
            name text,
            parent_dir integer
        )""")

        # Insert the root directory.
        c.execute("""insert into directory values (
            NULL,
            ?,
            ?
        )""", ('root', 0))

        # Commit all the changes we have made to the user database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        return

    def get_directory_info(self, directoryid=0, name='', parent_dir=1):
        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/document.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Search by directoryid.
        if directoryid:
            c.execute("""select * from directory where id=?""",
                (directoryid,))
        # Search by name and parent_dir.
        elif name and parent_dir:
            c.execute("""select * from directory where
                lower(name)=? and parent_dir=?""",
                (name.lower(), parent_dir))

        # Get 1 result, if any exist.
        row = c.fetchone()

        if row:
            res = {'id': row[0], 'name': row[1], 'parent_dir': row[2]}
        else:
            res = {}

        # Close the cursor that we created to the database and then close the
        # database itself.
        c.close()
        conn.close()
        return res

    def insert_directory(self, name, parent_dir=1):
        # The directory in the supplied folder with the supplied name does not
        # already exist.
        if not self.get_directory_info(name=name, parent_dir=parent_dir):
            # At this point, the user database must exist, so create a database
            # connection to the file.
            conn = connect(self.BASE_DIR + '/document.db')

            # Create the cursor to preform the queries.
            c = conn.cursor()

            c.execute("""insert into directory values
                (NULL, ?, ?)""", (name, parent_dir))

            # Commit all the changes we have made to the application database.
            conn.commit()

            # Close the cursor that we created to the database and then close
            # the database itself.
            c.close()
            conn.close()
            return True
        # The directory in the supplied folder with the supplied name already
        # exist.
        else:
            return False

    def init_table_stop_words(self, conn):
        """Create the stop_words table in the user database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Create the user table with the appropriate fields. The "id" field
        # denotes the user, not the username.
        c.execute("""create table stop_words (
            id integer primary key autoincrement,
            word text)""")

        # Insert a default words.
        c.execute("insert into stop_words values (NULL, ?)", ("a's",))
        c.execute("insert into stop_words values (NULL, ?)", ("able",))
        c.execute("insert into stop_words values (NULL, ?)", ("about",))
        c.execute("insert into stop_words values (NULL, ?)", ("above",))
        c.execute("insert into stop_words values (NULL, ?)", ("according",))
        c.execute("insert into stop_words values (NULL, ?)", ("accordingly",))
        c.execute("insert into stop_words values (NULL, ?)", ("across",))
        c.execute("insert into stop_words values (NULL, ?)", ("actually",))
        c.execute("insert into stop_words values (NULL, ?)", ("after",))
        c.execute("insert into stop_words values (NULL, ?)", ("afterwards",))
        c.execute("insert into stop_words values (NULL, ?)", ("again",))
        c.execute("insert into stop_words values (NULL, ?)", ("against",))
        c.execute("insert into stop_words values (NULL, ?)", ("ain't",))
        c.execute("insert into stop_words values (NULL, ?)", ("all",))
        c.execute("insert into stop_words values (NULL, ?)", ("allow",))
        c.execute("insert into stop_words values (NULL, ?)", ("allows",))
        c.execute("insert into stop_words values (NULL, ?)", ("almost",))
        c.execute("insert into stop_words values (NULL, ?)", ("alone",))
        c.execute("insert into stop_words values (NULL, ?)", ("along",))
        c.execute("insert into stop_words values (NULL, ?)", ("already",))
        c.execute("insert into stop_words values (NULL, ?)", ("also",))
        c.execute("insert into stop_words values (NULL, ?)", ("although",))
        c.execute("insert into stop_words values (NULL, ?)", ("always",))
        c.execute("insert into stop_words values (NULL, ?)", ("am",))
        c.execute("insert into stop_words values (NULL, ?)", ("among",))
        c.execute("insert into stop_words values (NULL, ?)", ("amongst",))
        c.execute("insert into stop_words values (NULL, ?)", ("an",))
        c.execute("insert into stop_words values (NULL, ?)", ("and",))
        c.execute("insert into stop_words values (NULL, ?)", ("another",))
        c.execute("insert into stop_words values (NULL, ?)", ("any",))
        c.execute("insert into stop_words values (NULL, ?)", ("anybody",))
        c.execute("insert into stop_words values (NULL, ?)", ("anyhow",))
        c.execute("insert into stop_words values (NULL, ?)", ("anyone",))
        c.execute("insert into stop_words values (NULL, ?)", ("anything",))
        c.execute("insert into stop_words values (NULL, ?)", ("anyway",))
        c.execute("insert into stop_words values (NULL, ?)", ("anyways",))
        c.execute("insert into stop_words values (NULL, ?)", ("anywhere",))
        c.execute("insert into stop_words values (NULL, ?)", ("apart",))
        c.execute("insert into stop_words values (NULL, ?)", ("appear",))
        c.execute("insert into stop_words values (NULL, ?)", ("appreciate",))
        c.execute("insert into stop_words values (NULL, ?)", ("appropriate",))
        c.execute("insert into stop_words values (NULL, ?)", ("are",))
        c.execute("insert into stop_words values (NULL, ?)", ("aren't",))
        c.execute("insert into stop_words values (NULL, ?)", ("around",))
        c.execute("insert into stop_words values (NULL, ?)", ("as",))
        c.execute("insert into stop_words values (NULL, ?)", ("aside",))
        c.execute("insert into stop_words values (NULL, ?)", ("ask",))
        c.execute("insert into stop_words values (NULL, ?)", ("asking",))
        c.execute("insert into stop_words values (NULL, ?)", ("associated",))
        c.execute("insert into stop_words values (NULL, ?)", ("at",))
        c.execute("insert into stop_words values (NULL, ?)", ("available",))
        c.execute("insert into stop_words values (NULL, ?)", ("away",))
        c.execute("insert into stop_words values (NULL, ?)", ("awfully",))
        c.execute("insert into stop_words values (NULL, ?)", ("be",))
        c.execute("insert into stop_words values (NULL, ?)", ("became",))
        c.execute("insert into stop_words values (NULL, ?)", ("because",))
        c.execute("insert into stop_words values (NULL, ?)", ("become",))
        c.execute("insert into stop_words values (NULL, ?)", ("becomes",))
        c.execute("insert into stop_words values (NULL, ?)", ("becoming",))
        c.execute("insert into stop_words values (NULL, ?)", ("been",))
        c.execute("insert into stop_words values (NULL, ?)", ("before",))
        c.execute("insert into stop_words values (NULL, ?)", ("beforehand",))
        c.execute("insert into stop_words values (NULL, ?)", ("behind",))
        c.execute("insert into stop_words values (NULL, ?)", ("being",))
        c.execute("insert into stop_words values (NULL, ?)", ("believe",))
        c.execute("insert into stop_words values (NULL, ?)", ("below",))
        c.execute("insert into stop_words values (NULL, ?)", ("beside",))
        c.execute("insert into stop_words values (NULL, ?)", ("besides",))
        c.execute("insert into stop_words values (NULL, ?)", ("best",))
        c.execute("insert into stop_words values (NULL, ?)", ("better",))
        c.execute("insert into stop_words values (NULL, ?)", ("between",))
        c.execute("insert into stop_words values (NULL, ?)", ("beyond",))
        c.execute("insert into stop_words values (NULL, ?)", ("both",))
        c.execute("insert into stop_words values (NULL, ?)", ("brief",))
        c.execute("insert into stop_words values (NULL, ?)", ("but",))
        c.execute("insert into stop_words values (NULL, ?)", ("by",))
        c.execute("insert into stop_words values (NULL, ?)", ("c'mon",))
        c.execute("insert into stop_words values (NULL, ?)", ("c's",))
        c.execute("insert into stop_words values (NULL, ?)", ("came",))
        c.execute("insert into stop_words values (NULL, ?)", ("can",))
        c.execute("insert into stop_words values (NULL, ?)", ("can't",))
        c.execute("insert into stop_words values (NULL, ?)", ("cannot",))
        c.execute("insert into stop_words values (NULL, ?)", ("cant",))
        c.execute("insert into stop_words values (NULL, ?)", ("cause",))
        c.execute("insert into stop_words values (NULL, ?)", ("causes",))
        c.execute("insert into stop_words values (NULL, ?)", ("certain",))
        c.execute("insert into stop_words values (NULL, ?)", ("certainly",))
        c.execute("insert into stop_words values (NULL, ?)", ("changes",))
        c.execute("insert into stop_words values (NULL, ?)", ("clearly",))
        c.execute("insert into stop_words values (NULL, ?)", ("co",))
        c.execute("insert into stop_words values (NULL, ?)", ("com",))
        c.execute("insert into stop_words values (NULL, ?)", ("come",))
        c.execute("insert into stop_words values (NULL, ?)", ("comes",))
        c.execute("insert into stop_words values (NULL, ?)", ("concerning",))
        c.execute("insert into stop_words values (NULL, ?)",
            ("consequently",))
        c.execute("insert into stop_words values (NULL, ?)", ("consider",))
        c.execute("insert into stop_words values (NULL, ?)", ("considering",))
        c.execute("insert into stop_words values (NULL, ?)", ("contain",))
        c.execute("insert into stop_words values (NULL, ?)", ("containing",))
        c.execute("insert into stop_words values (NULL, ?)", ("contains",))
        c.execute("insert into stop_words values (NULL, ?)",
            ("corresponding",))
        c.execute("insert into stop_words values (NULL, ?)", ("could",))
        c.execute("insert into stop_words values (NULL, ?)", ("couldn't",))
        c.execute("insert into stop_words values (NULL, ?)", ("course",))
        c.execute("insert into stop_words values (NULL, ?)", ("currently",))
        c.execute("insert into stop_words values (NULL, ?)", ("definitely",))
        c.execute("insert into stop_words values (NULL, ?)", ("described",))
        c.execute("insert into stop_words values (NULL, ?)", ("despite",))
        c.execute("insert into stop_words values (NULL, ?)", ("did",))
        c.execute("insert into stop_words values (NULL, ?)", ("didn't",))
        c.execute("insert into stop_words values (NULL, ?)", ("different",))
        c.execute("insert into stop_words values (NULL, ?)", ("do",))
        c.execute("insert into stop_words values (NULL, ?)", ("does",))
        c.execute("insert into stop_words values (NULL, ?)", ("doesn't",))
        c.execute("insert into stop_words values (NULL, ?)", ("doing",))
        c.execute("insert into stop_words values (NULL, ?)", ("don't",))
        c.execute("insert into stop_words values (NULL, ?)", ("done",))
        c.execute("insert into stop_words values (NULL, ?)", ("down",))
        c.execute("insert into stop_words values (NULL, ?)", ("downwards",))
        c.execute("insert into stop_words values (NULL, ?)", ("during",))
        c.execute("insert into stop_words values (NULL, ?)", ("each",))
        c.execute("insert into stop_words values (NULL, ?)", ("edu",))
        c.execute("insert into stop_words values (NULL, ?)", ("eg",))
        c.execute("insert into stop_words values (NULL, ?)", ("eight",))
        c.execute("insert into stop_words values (NULL, ?)", ("either",))
        c.execute("insert into stop_words values (NULL, ?)", ("else",))
        c.execute("insert into stop_words values (NULL, ?)", ("elsewhere",))
        c.execute("insert into stop_words values (NULL, ?)", ("enough",))
        c.execute("insert into stop_words values (NULL, ?)", ("entirely",))
        c.execute("insert into stop_words values (NULL, ?)", ("especially",))
        c.execute("insert into stop_words values (NULL, ?)", ("et",))
        c.execute("insert into stop_words values (NULL, ?)", ("etc",))
        c.execute("insert into stop_words values (NULL, ?)", ("even",))
        c.execute("insert into stop_words values (NULL, ?)", ("ever",))
        c.execute("insert into stop_words values (NULL, ?)", ("every",))
        c.execute("insert into stop_words values (NULL, ?)", ("everybody",))
        c.execute("insert into stop_words values (NULL, ?)", ("everyone",))
        c.execute("insert into stop_words values (NULL, ?)", ("everything",))
        c.execute("insert into stop_words values (NULL, ?)", ("everywhere",))
        c.execute("insert into stop_words values (NULL, ?)", ("ex",))
        c.execute("insert into stop_words values (NULL, ?)", ("exactly",))
        c.execute("insert into stop_words values (NULL, ?)", ("example",))
        c.execute("insert into stop_words values (NULL, ?)", ("except",))
        c.execute("insert into stop_words values (NULL, ?)", ("far",))
        c.execute("insert into stop_words values (NULL, ?)", ("few",))
        c.execute("insert into stop_words values (NULL, ?)", ("fifth",))
        c.execute("insert into stop_words values (NULL, ?)", ("first",))
        c.execute("insert into stop_words values (NULL, ?)", ("five",))
        c.execute("insert into stop_words values (NULL, ?)", ("followed",))
        c.execute("insert into stop_words values (NULL, ?)", ("following",))
        c.execute("insert into stop_words values (NULL, ?)", ("follows",))
        c.execute("insert into stop_words values (NULL, ?)", ("for",))
        c.execute("insert into stop_words values (NULL, ?)", ("former",))
        c.execute("insert into stop_words values (NULL, ?)", ("formerly",))
        c.execute("insert into stop_words values (NULL, ?)", ("forth",))
        c.execute("insert into stop_words values (NULL, ?)", ("four",))
        c.execute("insert into stop_words values (NULL, ?)", ("from",))
        c.execute("insert into stop_words values (NULL, ?)", ("further",))
        c.execute("insert into stop_words values (NULL, ?)", ("furthermore",))
        c.execute("insert into stop_words values (NULL, ?)", ("get",))
        c.execute("insert into stop_words values (NULL, ?)", ("gets",))
        c.execute("insert into stop_words values (NULL, ?)", ("getting",))
        c.execute("insert into stop_words values (NULL, ?)", ("given",))
        c.execute("insert into stop_words values (NULL, ?)", ("gives",))
        c.execute("insert into stop_words values (NULL, ?)", ("go",))
        c.execute("insert into stop_words values (NULL, ?)", ("goes",))
        c.execute("insert into stop_words values (NULL, ?)", ("going",))
        c.execute("insert into stop_words values (NULL, ?)", ("gone",))
        c.execute("insert into stop_words values (NULL, ?)", ("got",))
        c.execute("insert into stop_words values (NULL, ?)", ("gotten",))
        c.execute("insert into stop_words values (NULL, ?)", ("greetings",))
        c.execute("insert into stop_words values (NULL, ?)", ("had",))
        c.execute("insert into stop_words values (NULL, ?)", ("hadn't",))
        c.execute("insert into stop_words values (NULL, ?)", ("happens",))
        c.execute("insert into stop_words values (NULL, ?)", ("hardly",))
        c.execute("insert into stop_words values (NULL, ?)", ("has",))
        c.execute("insert into stop_words values (NULL, ?)", ("hasn't",))
        c.execute("insert into stop_words values (NULL, ?)", ("have",))
        c.execute("insert into stop_words values (NULL, ?)", ("haven't",))
        c.execute("insert into stop_words values (NULL, ?)", ("having",))
        c.execute("insert into stop_words values (NULL, ?)", ("he",))
        c.execute("insert into stop_words values (NULL, ?)", ("he's",))
        c.execute("insert into stop_words values (NULL, ?)", ("hello",))
        c.execute("insert into stop_words values (NULL, ?)", ("help",))
        c.execute("insert into stop_words values (NULL, ?)", ("hence",))
        c.execute("insert into stop_words values (NULL, ?)", ("her",))
        c.execute("insert into stop_words values (NULL, ?)", ("here",))
        c.execute("insert into stop_words values (NULL, ?)", ("here's",))
        c.execute("insert into stop_words values (NULL, ?)", ("hereafter",))
        c.execute("insert into stop_words values (NULL, ?)", ("hereby",))
        c.execute("insert into stop_words values (NULL, ?)", ("herein",))
        c.execute("insert into stop_words values (NULL, ?)", ("hereupon",))
        c.execute("insert into stop_words values (NULL, ?)", ("hers",))
        c.execute("insert into stop_words values (NULL, ?)", ("herself",))
        c.execute("insert into stop_words values (NULL, ?)", ("hi",))
        c.execute("insert into stop_words values (NULL, ?)", ("him",))
        c.execute("insert into stop_words values (NULL, ?)", ("himself",))
        c.execute("insert into stop_words values (NULL, ?)", ("his",))
        c.execute("insert into stop_words values (NULL, ?)", ("hither",))
        c.execute("insert into stop_words values (NULL, ?)", ("hopefully",))
        c.execute("insert into stop_words values (NULL, ?)", ("how",))
        c.execute("insert into stop_words values (NULL, ?)", ("howbeit",))
        c.execute("insert into stop_words values (NULL, ?)", ("however",))
        c.execute("insert into stop_words values (NULL, ?)", ("i'd",))
        c.execute("insert into stop_words values (NULL, ?)", ("i'll",))
        c.execute("insert into stop_words values (NULL, ?)", ("i'm",))
        c.execute("insert into stop_words values (NULL, ?)", ("i've",))
        c.execute("insert into stop_words values (NULL, ?)", ("ie",))
        c.execute("insert into stop_words values (NULL, ?)", ("if",))
        c.execute("insert into stop_words values (NULL, ?)", ("ignored",))
        c.execute("insert into stop_words values (NULL, ?)", ("immediate",))
        c.execute("insert into stop_words values (NULL, ?)", ("in",))
        c.execute("insert into stop_words values (NULL, ?)", ("inasmuch",))
        c.execute("insert into stop_words values (NULL, ?)", ("inc",))
        c.execute("insert into stop_words values (NULL, ?)", ("indeed",))
        c.execute("insert into stop_words values (NULL, ?)", ("indicate",))
        c.execute("insert into stop_words values (NULL, ?)", ("indicated",))
        c.execute("insert into stop_words values (NULL, ?)", ("indicates",))
        c.execute("insert into stop_words values (NULL, ?)", ("inner",))
        c.execute("insert into stop_words values (NULL, ?)", ("insofar",))
        c.execute("insert into stop_words values (NULL, ?)", ("instead",))
        c.execute("insert into stop_words values (NULL, ?)", ("into",))
        c.execute("insert into stop_words values (NULL, ?)", ("inward",))
        c.execute("insert into stop_words values (NULL, ?)", ("is",))
        c.execute("insert into stop_words values (NULL, ?)", ("isn't",))
        c.execute("insert into stop_words values (NULL, ?)", ("it",))
        c.execute("insert into stop_words values (NULL, ?)", ("it'd",))
        c.execute("insert into stop_words values (NULL, ?)", ("it'll",))
        c.execute("insert into stop_words values (NULL, ?)", ("it's",))
        c.execute("insert into stop_words values (NULL, ?)", ("its",))
        c.execute("insert into stop_words values (NULL, ?)", ("itself",))
        c.execute("insert into stop_words values (NULL, ?)", ("just",))
        c.execute("insert into stop_words values (NULL, ?)", ("keep",))
        c.execute("insert into stop_words values (NULL, ?)", ("keeps",))
        c.execute("insert into stop_words values (NULL, ?)", ("kept",))
        c.execute("insert into stop_words values (NULL, ?)", ("know",))
        c.execute("insert into stop_words values (NULL, ?)", ("known",))
        c.execute("insert into stop_words values (NULL, ?)", ("knows",))
        c.execute("insert into stop_words values (NULL, ?)", ("last",))
        c.execute("insert into stop_words values (NULL, ?)", ("lately",))
        c.execute("insert into stop_words values (NULL, ?)", ("later",))
        c.execute("insert into stop_words values (NULL, ?)", ("latter",))
        c.execute("insert into stop_words values (NULL, ?)", ("latterly",))
        c.execute("insert into stop_words values (NULL, ?)", ("least",))
        c.execute("insert into stop_words values (NULL, ?)", ("less",))
        c.execute("insert into stop_words values (NULL, ?)", ("lest",))
        c.execute("insert into stop_words values (NULL, ?)", ("let",))
        c.execute("insert into stop_words values (NULL, ?)", ("let's",))
        c.execute("insert into stop_words values (NULL, ?)", ("like",))
        c.execute("insert into stop_words values (NULL, ?)", ("liked",))
        c.execute("insert into stop_words values (NULL, ?)", ("likely",))
        c.execute("insert into stop_words values (NULL, ?)", ("little",))
        c.execute("insert into stop_words values (NULL, ?)", ("look",))
        c.execute("insert into stop_words values (NULL, ?)", ("looking",))
        c.execute("insert into stop_words values (NULL, ?)", ("looks",))
        c.execute("insert into stop_words values (NULL, ?)", ("ltd",))
        c.execute("insert into stop_words values (NULL, ?)", ("mainly",))
        c.execute("insert into stop_words values (NULL, ?)", ("many",))
        c.execute("insert into stop_words values (NULL, ?)", ("may",))
        c.execute("insert into stop_words values (NULL, ?)", ("maybe",))
        c.execute("insert into stop_words values (NULL, ?)", ("me",))
        c.execute("insert into stop_words values (NULL, ?)", ("mean",))
        c.execute("insert into stop_words values (NULL, ?)", ("meanwhile",))
        c.execute("insert into stop_words values (NULL, ?)", ("merely",))
        c.execute("insert into stop_words values (NULL, ?)", ("might",))
        c.execute("insert into stop_words values (NULL, ?)", ("more",))
        c.execute("insert into stop_words values (NULL, ?)", ("moreover",))
        c.execute("insert into stop_words values (NULL, ?)", ("most",))
        c.execute("insert into stop_words values (NULL, ?)", ("mostly",))
        c.execute("insert into stop_words values (NULL, ?)", ("much",))
        c.execute("insert into stop_words values (NULL, ?)", ("must",))
        c.execute("insert into stop_words values (NULL, ?)", ("my",))
        c.execute("insert into stop_words values (NULL, ?)", ("myself",))
        c.execute("insert into stop_words values (NULL, ?)", ("name",))
        c.execute("insert into stop_words values (NULL, ?)", ("namely",))
        c.execute("insert into stop_words values (NULL, ?)", ("nd",))
        c.execute("insert into stop_words values (NULL, ?)", ("near",))
        c.execute("insert into stop_words values (NULL, ?)", ("nearly",))
        c.execute("insert into stop_words values (NULL, ?)", ("necessary",))
        c.execute("insert into stop_words values (NULL, ?)", ("need",))
        c.execute("insert into stop_words values (NULL, ?)", ("needs",))
        c.execute("insert into stop_words values (NULL, ?)", ("neither",))
        c.execute("insert into stop_words values (NULL, ?)", ("never",))
        c.execute("insert into stop_words values (NULL, ?)",
            ("nevertheless",))
        c.execute("insert into stop_words values (NULL, ?)", ("new",))
        c.execute("insert into stop_words values (NULL, ?)", ("next",))
        c.execute("insert into stop_words values (NULL, ?)", ("nine",))
        c.execute("insert into stop_words values (NULL, ?)", ("no",))
        c.execute("insert into stop_words values (NULL, ?)", ("nobody",))
        c.execute("insert into stop_words values (NULL, ?)", ("non",))
        c.execute("insert into stop_words values (NULL, ?)", ("none",))
        c.execute("insert into stop_words values (NULL, ?)", ("noone",))
        c.execute("insert into stop_words values (NULL, ?)", ("nor",))
        c.execute("insert into stop_words values (NULL, ?)", ("normally",))
        c.execute("insert into stop_words values (NULL, ?)", ("not",))
        c.execute("insert into stop_words values (NULL, ?)", ("nothing",))
        c.execute("insert into stop_words values (NULL, ?)", ("novel",))
        c.execute("insert into stop_words values (NULL, ?)", ("now",))
        c.execute("insert into stop_words values (NULL, ?)", ("nowhere",))
        c.execute("insert into stop_words values (NULL, ?)", ("obviously",))
        c.execute("insert into stop_words values (NULL, ?)", ("of",))
        c.execute("insert into stop_words values (NULL, ?)", ("off",))
        c.execute("insert into stop_words values (NULL, ?)", ("often",))
        c.execute("insert into stop_words values (NULL, ?)", ("oh",))
        c.execute("insert into stop_words values (NULL, ?)", ("ok",))
        c.execute("insert into stop_words values (NULL, ?)", ("okay",))
        c.execute("insert into stop_words values (NULL, ?)", ("old",))
        c.execute("insert into stop_words values (NULL, ?)", ("on",))
        c.execute("insert into stop_words values (NULL, ?)", ("once",))
        c.execute("insert into stop_words values (NULL, ?)", ("one",))
        c.execute("insert into stop_words values (NULL, ?)", ("ones",))
        c.execute("insert into stop_words values (NULL, ?)", ("only",))
        c.execute("insert into stop_words values (NULL, ?)", ("onto",))
        c.execute("insert into stop_words values (NULL, ?)", ("or",))
        c.execute("insert into stop_words values (NULL, ?)", ("other",))
        c.execute("insert into stop_words values (NULL, ?)", ("others",))
        c.execute("insert into stop_words values (NULL, ?)", ("otherwise",))
        c.execute("insert into stop_words values (NULL, ?)", ("ought",))
        c.execute("insert into stop_words values (NULL, ?)", ("our",))
        c.execute("insert into stop_words values (NULL, ?)", ("ours",))
        c.execute("insert into stop_words values (NULL, ?)", ("ourselves",))
        c.execute("insert into stop_words values (NULL, ?)", ("out",))
        c.execute("insert into stop_words values (NULL, ?)", ("outside",))
        c.execute("insert into stop_words values (NULL, ?)", ("over",))
        c.execute("insert into stop_words values (NULL, ?)", ("overall",))
        c.execute("insert into stop_words values (NULL, ?)", ("own",))
        c.execute("insert into stop_words values (NULL, ?)", ("particular",))
        c.execute("insert into stop_words values (NULL, ?)",
            ("particularly",))
        c.execute("insert into stop_words values (NULL, ?)", ("per",))
        c.execute("insert into stop_words values (NULL, ?)", ("perhaps",))
        c.execute("insert into stop_words values (NULL, ?)", ("placed",))
        c.execute("insert into stop_words values (NULL, ?)", ("please",))
        c.execute("insert into stop_words values (NULL, ?)", ("plus",))
        c.execute("insert into stop_words values (NULL, ?)", ("possible",))
        c.execute("insert into stop_words values (NULL, ?)", ("presumably",))
        c.execute("insert into stop_words values (NULL, ?)", ("probably",))
        c.execute("insert into stop_words values (NULL, ?)", ("provides",))
        c.execute("insert into stop_words values (NULL, ?)", ("que",))
        c.execute("insert into stop_words values (NULL, ?)", ("quite",))
        c.execute("insert into stop_words values (NULL, ?)", ("qv",))
        c.execute("insert into stop_words values (NULL, ?)", ("rather",))
        c.execute("insert into stop_words values (NULL, ?)", ("rd",))
        c.execute("insert into stop_words values (NULL, ?)", ("re",))
        c.execute("insert into stop_words values (NULL, ?)", ("really",))
        c.execute("insert into stop_words values (NULL, ?)", ("reasonably",))
        c.execute("insert into stop_words values (NULL, ?)", ("regarding",))
        c.execute("insert into stop_words values (NULL, ?)", ("regardless",))
        c.execute("insert into stop_words values (NULL, ?)", ("regards",))
        c.execute("insert into stop_words values (NULL, ?)", ("relatively",))
        c.execute("insert into stop_words values (NULL, ?)",
            ("respectively",))
        c.execute("insert into stop_words values (NULL, ?)", ("right",))
        c.execute("insert into stop_words values (NULL, ?)", ("said",))
        c.execute("insert into stop_words values (NULL, ?)", ("same",))
        c.execute("insert into stop_words values (NULL, ?)", ("saw",))
        c.execute("insert into stop_words values (NULL, ?)", ("say",))
        c.execute("insert into stop_words values (NULL, ?)", ("saying",))
        c.execute("insert into stop_words values (NULL, ?)", ("says",))
        c.execute("insert into stop_words values (NULL, ?)", ("second",))
        c.execute("insert into stop_words values (NULL, ?)", ("secondly",))
        c.execute("insert into stop_words values (NULL, ?)", ("see",))
        c.execute("insert into stop_words values (NULL, ?)", ("seeing",))
        c.execute("insert into stop_words values (NULL, ?)", ("seem",))
        c.execute("insert into stop_words values (NULL, ?)", ("seemed",))
        c.execute("insert into stop_words values (NULL, ?)", ("seeming",))
        c.execute("insert into stop_words values (NULL, ?)", ("seems",))
        c.execute("insert into stop_words values (NULL, ?)", ("seen",))
        c.execute("insert into stop_words values (NULL, ?)", ("self",))
        c.execute("insert into stop_words values (NULL, ?)", ("selves",))
        c.execute("insert into stop_words values (NULL, ?)", ("sensible",))
        c.execute("insert into stop_words values (NULL, ?)", ("sent",))
        c.execute("insert into stop_words values (NULL, ?)", ("serious",))
        c.execute("insert into stop_words values (NULL, ?)", ("seriously",))
        c.execute("insert into stop_words values (NULL, ?)", ("seven",))
        c.execute("insert into stop_words values (NULL, ?)", ("several",))
        c.execute("insert into stop_words values (NULL, ?)", ("shall",))
        c.execute("insert into stop_words values (NULL, ?)", ("she",))
        c.execute("insert into stop_words values (NULL, ?)", ("should",))
        c.execute("insert into stop_words values (NULL, ?)", ("shouldn't",))
        c.execute("insert into stop_words values (NULL, ?)", ("since",))
        c.execute("insert into stop_words values (NULL, ?)", ("six",))
        c.execute("insert into stop_words values (NULL, ?)", ("so",))
        c.execute("insert into stop_words values (NULL, ?)", ("some",))
        c.execute("insert into stop_words values (NULL, ?)", ("somebody",))
        c.execute("insert into stop_words values (NULL, ?)", ("somehow",))
        c.execute("insert into stop_words values (NULL, ?)", ("someone",))
        c.execute("insert into stop_words values (NULL, ?)", ("something",))
        c.execute("insert into stop_words values (NULL, ?)", ("sometime",))
        c.execute("insert into stop_words values (NULL, ?)", ("sometimes",))
        c.execute("insert into stop_words values (NULL, ?)", ("somewhat",))
        c.execute("insert into stop_words values (NULL, ?)", ("somewhere",))
        c.execute("insert into stop_words values (NULL, ?)", ("soon",))
        c.execute("insert into stop_words values (NULL, ?)", ("sorry",))
        c.execute("insert into stop_words values (NULL, ?)", ("specified",))
        c.execute("insert into stop_words values (NULL, ?)", ("specify",))
        c.execute("insert into stop_words values (NULL, ?)", ("specifying",))
        c.execute("insert into stop_words values (NULL, ?)", ("still",))
        c.execute("insert into stop_words values (NULL, ?)", ("sub",))
        c.execute("insert into stop_words values (NULL, ?)", ("such",))
        c.execute("insert into stop_words values (NULL, ?)", ("sup",))
        c.execute("insert into stop_words values (NULL, ?)", ("sure",))
        c.execute("insert into stop_words values (NULL, ?)", ("t's",))
        c.execute("insert into stop_words values (NULL, ?)", ("take",))
        c.execute("insert into stop_words values (NULL, ?)", ("taken",))
        c.execute("insert into stop_words values (NULL, ?)", ("tell",))
        c.execute("insert into stop_words values (NULL, ?)", ("tends",))
        c.execute("insert into stop_words values (NULL, ?)", ("th",))
        c.execute("insert into stop_words values (NULL, ?)", ("than",))
        c.execute("insert into stop_words values (NULL, ?)", ("thank",))
        c.execute("insert into stop_words values (NULL, ?)", ("thanks",))
        c.execute("insert into stop_words values (NULL, ?)", ("thanx",))
        c.execute("insert into stop_words values (NULL, ?)", ("that",))
        c.execute("insert into stop_words values (NULL, ?)", ("that's",))
        c.execute("insert into stop_words values (NULL, ?)", ("thats",))
        c.execute("insert into stop_words values (NULL, ?)", ("the",))
        c.execute("insert into stop_words values (NULL, ?)", ("their",))
        c.execute("insert into stop_words values (NULL, ?)", ("theirs",))
        c.execute("insert into stop_words values (NULL, ?)", ("them",))
        c.execute("insert into stop_words values (NULL, ?)", ("themselves",))
        c.execute("insert into stop_words values (NULL, ?)", ("then",))
        c.execute("insert into stop_words values (NULL, ?)", ("thence",))
        c.execute("insert into stop_words values (NULL, ?)", ("there",))
        c.execute("insert into stop_words values (NULL, ?)", ("there's",))
        c.execute("insert into stop_words values (NULL, ?)", ("thereafter",))
        c.execute("insert into stop_words values (NULL, ?)", ("thereby",))
        c.execute("insert into stop_words values (NULL, ?)", ("therefore",))
        c.execute("insert into stop_words values (NULL, ?)", ("therein",))
        c.execute("insert into stop_words values (NULL, ?)", ("theres",))
        c.execute("insert into stop_words values (NULL, ?)", ("thereupon",))
        c.execute("insert into stop_words values (NULL, ?)", ("these",))
        c.execute("insert into stop_words values (NULL, ?)", ("they",))
        c.execute("insert into stop_words values (NULL, ?)", ("they'd",))
        c.execute("insert into stop_words values (NULL, ?)", ("they'll",))
        c.execute("insert into stop_words values (NULL, ?)", ("they're",))
        c.execute("insert into stop_words values (NULL, ?)", ("they've",))
        c.execute("insert into stop_words values (NULL, ?)", ("think",))
        c.execute("insert into stop_words values (NULL, ?)", ("third",))
        c.execute("insert into stop_words values (NULL, ?)", ("this",))
        c.execute("insert into stop_words values (NULL, ?)", ("thorough",))
        c.execute("insert into stop_words values (NULL, ?)", ("thoroughly",))
        c.execute("insert into stop_words values (NULL, ?)", ("those",))
        c.execute("insert into stop_words values (NULL, ?)", ("though",))
        c.execute("insert into stop_words values (NULL, ?)", ("three",))
        c.execute("insert into stop_words values (NULL, ?)", ("through",))
        c.execute("insert into stop_words values (NULL, ?)", ("throughout",))
        c.execute("insert into stop_words values (NULL, ?)", ("thru",))
        c.execute("insert into stop_words values (NULL, ?)", ("thus",))
        c.execute("insert into stop_words values (NULL, ?)", ("to",))
        c.execute("insert into stop_words values (NULL, ?)", ("together",))
        c.execute("insert into stop_words values (NULL, ?)", ("too",))
        c.execute("insert into stop_words values (NULL, ?)", ("took",))
        c.execute("insert into stop_words values (NULL, ?)", ("toward",))
        c.execute("insert into stop_words values (NULL, ?)", ("towards",))
        c.execute("insert into stop_words values (NULL, ?)", ("tried",))
        c.execute("insert into stop_words values (NULL, ?)", ("tries",))
        c.execute("insert into stop_words values (NULL, ?)", ("truly",))
        c.execute("insert into stop_words values (NULL, ?)", ("try",))
        c.execute("insert into stop_words values (NULL, ?)", ("trying",))
        c.execute("insert into stop_words values (NULL, ?)", ("twice",))
        c.execute("insert into stop_words values (NULL, ?)", ("two",))
        c.execute("insert into stop_words values (NULL, ?)", ("un",))
        c.execute("insert into stop_words values (NULL, ?)", ("under",))
        c.execute("insert into stop_words values (NULL, ?)",
            ("unfortunately",))
        c.execute("insert into stop_words values (NULL, ?)", ("unless",))
        c.execute("insert into stop_words values (NULL, ?)", ("unlikely",))
        c.execute("insert into stop_words values (NULL, ?)", ("until",))
        c.execute("insert into stop_words values (NULL, ?)", ("unto",))
        c.execute("insert into stop_words values (NULL, ?)", ("up",))
        c.execute("insert into stop_words values (NULL, ?)", ("upon",))
        c.execute("insert into stop_words values (NULL, ?)", ("us",))
        c.execute("insert into stop_words values (NULL, ?)", ("use",))
        c.execute("insert into stop_words values (NULL, ?)", ("used",))
        c.execute("insert into stop_words values (NULL, ?)", ("useful",))
        c.execute("insert into stop_words values (NULL, ?)", ("uses",))
        c.execute("insert into stop_words values (NULL, ?)", ("using",))
        c.execute("insert into stop_words values (NULL, ?)", ("usually",))
        c.execute("insert into stop_words values (NULL, ?)", ("value",))
        c.execute("insert into stop_words values (NULL, ?)", ("various",))
        c.execute("insert into stop_words values (NULL, ?)", ("very",))
        c.execute("insert into stop_words values (NULL, ?)", ("via",))
        c.execute("insert into stop_words values (NULL, ?)", ("viz",))
        c.execute("insert into stop_words values (NULL, ?)", ("vs",))
        c.execute("insert into stop_words values (NULL, ?)", ("want",))
        c.execute("insert into stop_words values (NULL, ?)", ("wants",))
        c.execute("insert into stop_words values (NULL, ?)", ("was",))
        c.execute("insert into stop_words values (NULL, ?)", ("wasn't",))
        c.execute("insert into stop_words values (NULL, ?)", ("way",))
        c.execute("insert into stop_words values (NULL, ?)", ("we",))
        c.execute("insert into stop_words values (NULL, ?)", ("we'd",))
        c.execute("insert into stop_words values (NULL, ?)", ("we'll",))
        c.execute("insert into stop_words values (NULL, ?)", ("we're",))
        c.execute("insert into stop_words values (NULL, ?)", ("we've",))
        c.execute("insert into stop_words values (NULL, ?)", ("welcome",))
        c.execute("insert into stop_words values (NULL, ?)", ("well",))
        c.execute("insert into stop_words values (NULL, ?)", ("went",))
        c.execute("insert into stop_words values (NULL, ?)", ("were",))
        c.execute("insert into stop_words values (NULL, ?)", ("weren't",))
        c.execute("insert into stop_words values (NULL, ?)", ("what",))
        c.execute("insert into stop_words values (NULL, ?)", ("what's",))
        c.execute("insert into stop_words values (NULL, ?)", ("whatever",))
        c.execute("insert into stop_words values (NULL, ?)", ("when",))
        c.execute("insert into stop_words values (NULL, ?)", ("whence",))
        c.execute("insert into stop_words values (NULL, ?)", ("whenever",))
        c.execute("insert into stop_words values (NULL, ?)", ("where",))
        c.execute("insert into stop_words values (NULL, ?)", ("where's",))
        c.execute("insert into stop_words values (NULL, ?)", ("whereafter",))
        c.execute("insert into stop_words values (NULL, ?)", ("whereas",))
        c.execute("insert into stop_words values (NULL, ?)", ("whereby",))
        c.execute("insert into stop_words values (NULL, ?)", ("wherein",))
        c.execute("insert into stop_words values (NULL, ?)", ("whereupon",))
        c.execute("insert into stop_words values (NULL, ?)", ("wherever",))
        c.execute("insert into stop_words values (NULL, ?)", ("whether",))
        c.execute("insert into stop_words values (NULL, ?)", ("which",))
        c.execute("insert into stop_words values (NULL, ?)", ("while",))
        c.execute("insert into stop_words values (NULL, ?)", ("whither",))
        c.execute("insert into stop_words values (NULL, ?)", ("who",))
        c.execute("insert into stop_words values (NULL, ?)", ("who's",))
        c.execute("insert into stop_words values (NULL, ?)", ("whoever",))
        c.execute("insert into stop_words values (NULL, ?)", ("whole",))
        c.execute("insert into stop_words values (NULL, ?)", ("whom",))
        c.execute("insert into stop_words values (NULL, ?)", ("whose",))
        c.execute("insert into stop_words values (NULL, ?)", ("why",))
        c.execute("insert into stop_words values (NULL, ?)", ("will",))
        c.execute("insert into stop_words values (NULL, ?)", ("willing",))
        c.execute("insert into stop_words values (NULL, ?)", ("wish",))
        c.execute("insert into stop_words values (NULL, ?)", ("with",))
        c.execute("insert into stop_words values (NULL, ?)", ("within",))
        c.execute("insert into stop_words values (NULL, ?)", ("without",))
        c.execute("insert into stop_words values (NULL, ?)", ("won't",))
        c.execute("insert into stop_words values (NULL, ?)", ("wonder",))
        c.execute("insert into stop_words values (NULL, ?)", ("would",))
        c.execute("insert into stop_words values (NULL, ?)", ("wouldn't",))
        c.execute("insert into stop_words values (NULL, ?)", ("yes",))
        c.execute("insert into stop_words values (NULL, ?)", ("yet",))
        c.execute("insert into stop_words values (NULL, ?)", ("you",))
        c.execute("insert into stop_words values (NULL, ?)", ("you'd",))
        c.execute("insert into stop_words values (NULL, ?)", ("you'll",))
        c.execute("insert into stop_words values (NULL, ?)", ("you're",))
        c.execute("insert into stop_words values (NULL, ?)", ("you've",))
        c.execute("insert into stop_words values (NULL, ?)", ("your",))
        c.execute("insert into stop_words values (NULL, ?)", ("yours",))
        c.execute("insert into stop_words values (NULL, ?)", ("yourself",))
        c.execute("insert into stop_words values (NULL, ?)", ("yourselves",))
        c.execute("insert into stop_words values (NULL, ?)", ("zero",))

        # Commit all the changes we have made to the user database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        return

    def get_stop_words_info(self, wordid=0, word=''):
        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/index.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Search by wordid.
        if wordid:
            c.execute("""select * from stop_words where id=?""", (wordid,))
        # Search by word.
        elif word:
            c.execute("""select * from stop_words where lower(word)=?""",
                (word.lower(),))

        # Get 1 result, if any exist.
        row = c.fetchone()

        if row:
            res = {'id': row[0], 'word': row[1]}
        else:
            res = {}

        # Close the cursor that we created to the database and then close the
        # database itself.
        c.close()
        conn.close()
        return res

    def insert_stop_words(self, word):
        # The supplied word does not already exist in the table.
        if not self.get_stop_words_info(word=word):
            # At this point, the user database must exist, so create a database
            # connection to the file.
            conn = connect(self.BASE_DIR + '/index.db')

            # Create the cursor to preform the queries.
            c = conn.cursor()

            c.execute("""insert into stop_words values
                (NULL, ?)""", (word,))

            # Commit all the changes we have made to the application database.
            conn.commit()

            # Close the cursor that we created to the database and then close
            # the database itself.
            c.close()
            conn.close()
            return True
        # The supplied word already exist in the table.
        else:
            return False

    def init_table_index_word(self, conn):
        """Create the index table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Create the index_word table with the appropriate fields. The "id"
        # field denotes the directory, not the name field.
        c.execute("""create table index_word (
            id integer primary key autoincrement,
            word text
        )""")

        # Commit all the changes we have made to the index database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        return

    def get_index_word_info(self, wordid=0, word=''):
        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/index.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Search by wordid.
        if wordid:
            c.execute("""select * from index_word where id=?""", (wordid,))
        # Search by word.
        elif word:
            c.execute("""select * from index_word where lower(word)=?""",
                (word.lower(),))

        # Get 1 result, if any exist.
        row = c.fetchone()

        if row:
            res = {'id': row[0], 'word': row[1]}
        else:
            res = {}

        # Close the cursor that we created to the database and then close the
        # database itself.
        c.close()
        conn.close()
        return res

    def insert_index_word(self, word):
        # The supplied word does not already exist in the table.
        if not self.get_index_word_info(word=word):
            # At this point, the user database must exist, so create a database
            # connection to the file.
            conn = connect(self.BASE_DIR + '/index.db')

            # Create the cursor to preform the queries.
            c = conn.cursor()

            c.execute("""insert into index_word values
                (NULL, ?)""", (word,))

            # Commit all the changes we have made to the application database.
            conn.commit()

            # Close the cursor that we created to the database and then close
            # the database itself.
            c.close()
            conn.close()
            return True
        # The supplied word already exist in the table.
        else:
            return False

    def init_table_index_ref(self, conn):
        """Create the index_ref table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Create the index_ref table with the appropriate fields. The "id"
        # field denotes the directory, not the name field.
        c.execute("""create table index_ref (
            id integer primary key autoincrement,
            wordid integer,
            docid integer,
            line integer,
            column integer,
            branch_word text
        )""")

        # Commit all the changes we have made to the index database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        return

    def get_index_ref_info(self, refid=0,
        wordid=0, docid=0, line=0, column=0):
        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = connect(self.BASE_DIR + '/index.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Search by refid.
        if refid:
            c.execute("""select * from index_ref where id=?""", (refid,))
        # Search by wordid and docid and line and column.
        elif wordid and docid and line and column:
            c.execute("""select * from index_ref where
                wordid=? and docid=? and line=? and column=?""",
                (wordid, docid, line, column))

        # Get 1 result, if any exist.
        row = c.fetchone()

        if row:
            res = {'id': row[0], 'wordid': row[1], 'docid': row[2],
                'line': row[3], 'column': row[4], 'branch_word': row[5]}
        else:
            res = {}

        # Close the cursor that we created to the database and then close the
        # database itself.
        c.close()
        conn.close()
        return res

    def insert_index_ref(self, wordid, docid, line, column, branch_word):
        # The supplied reference does not already exist in the table.
        if not self.get_index_ref_info(
            wordid=wordid, docid=docid, line=line, column=column):
            # At this point, the user database must exist, so create a database
            # connection to the file.
            conn = connect(self.BASE_DIR + '/index.db')

            # Create the cursor to preform the queries.
            c = conn.cursor()

            c.execute("""insert into index_ref values
                (NULL, ?, ?, ?, ?, ?)""",
                (wordid, docid, line, column, branch_word))

            # Commit all the changes we have made to the application database.
            conn.commit()

            # Close the cursor that we created to the database and then close
            # the database itself.
            c.close()
            conn.close()
            return True
        # The supplied reference already exist in the table.
        else:
            return False

    def print_userDB(self):
        conn = connect(self.BASE_DIR + '/user.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        print 'user DB:'
        c.execute("""select * from user""")

        for row in c:
            print row

        print '\nusergroup DB:'
        c.execute("""select * from usergroup""")

        for row in c:
            print row

        c.close()
        conn.close()
        return

    def print_documentDB(self):
        conn = connect(self.BASE_DIR + '/document.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        print 'document DB:'
        c.execute("""select * from document""")

        for row in c:
            print row

        print '\ncomment DB:'
        c.execute("""select * from comment""")

        for row in c:
            print row

        print '\ncomplaint DB:'
        c.execute("""select * from complaint""")

        for row in c:
            print row

        print '\nmember DB:'
        c.execute("""select * from member""")

        for row in c:
            print row

        print '\ninvitation DB:'
        c.execute("""select * from invitation""")

        for row in c:
            print row

        print '\ndirectory DB:'
        c.execute("""select * from directory""")

        for row in c:
            print row

        c.close()
        conn.close()
        return

    def print_indexDB(self):
        conn = connect(self.BASE_DIR + '/index.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

#        print 'stop_words DB:'
#        c.execute("""select * from stop_words""")

#        for row in c:
#            print row

#        print '\nindex_word DB:'
#        c.execute("""select * from index_word""")

#        for row in c:
#            print row

        print '\nindex_ref DB:'
        c.execute("""select * from index_ref""")

        for row in c:
            print row

        c.close()
        conn.close()
        return

    def insert_table_user(self, package):
        """Insert a user into the user table using the information contained
        within the package. The "package" should be a dictionary with the
        following keys:
            username    =>  New user's username.
            password    =>  New user's password.
            email       =>  New user's email.
            usergroup   =>  New user's usergroup."""
        # Create the cursor to preform the queries.
        conn = connect(self.BASE_DIR + '/user.db')

        # Create the cursor to preform the queries.
        c = conn.cursor()

        t = (package['username'], package['password'],
            package['email'], package['usergroup'], 0)
        c.execute("""insert into user values (
            NULL, ?, ?, ?, ?, ?
        )""", t)

        # Commit all the changes we have made to the user database.
        conn.commit()

        # Close the cursor that we created to the database.
        c.close()
        conn.close()
        return

    def select_table_user(self, query, select):
        """Selects a user(s) from the user table using the key/value pairs
        contained within the query dictionary and returns the values for the
        columns contained in the select list."""
        conn = connect(self.BASE_DIR + '/user.db')
        c = conn.cursor()

        str_query = ''
        for pair in query.items():
            str_query += pair[0] + '=? AND '
        str_query = str_query[:-5]

        t = tuple(query.values())
        c.execute("""select * from user where """ + str_query, t)

        res = []
        for row in c:
            qdic = {'id': row[0], 'username': row[1], 'password': row[2],
                'email': row[3], 'usergroup': row[4], 'infraction': row[5]}
            li = []
            for field in select:
                li.append(qdic[field])
            res.append(li)

        conn.commit()
        c.close()
        conn.close()
        return res

if __name__ == "__main__":
    dbm = DBManager()
#    dbm.print_userDB()
#    print ''
#    dbm.print_documentDB()
#    print ''
#    dbm.print_indexDB()
#    q = {'username': 'admin'}
#    s = ['email', 'infraction']
#    print dbm.select_table_user(q, s)
    print dbm.get_user_info(username='ash')
