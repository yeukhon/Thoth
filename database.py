#  database.py
#
#  Copyright 2012 Kevin Ramdath <KRPent@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import os
import sqlite3
from time import time
from md5 import new


class Database(object):
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
        conn = sqlite3.connect(self.BASE_DIR + '/user.db')

        # Create the application table and insert the default values.
        self.init_table_application(conn)

        # Create the user table and insert the default values.
        self.init_table_user(conn)

        # Create the usergroup table and insert the default values.
        self.init_table_usergroup(conn)

        # Create the invitation table and insert the default values.
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
        conn = sqlite3.connect(self.BASE_DIR + '/document.db')

        # Create the document table and insert the default values.
        self.init_table_document(conn)

        # Create the comment table and insert the default values.
        self.init_table_comment(conn)

        # Create the complaint table and insert the default values.
        self.init_table_complaint(conn)

        # Create the directory table and insert the default values.
        self.init_table_directory(conn)

        # Create the member table and insert the default values.
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
        conn = sqlite3.connect(self.BASE_DIR + '/index.db')

        # Create the stop_words table and insert the default values.
        self.init_table_stop_words(conn)

        # Create the index_word table and insert the default values.
        self.init_table_index_word(conn)

        # Create the index_ref table and insert the default values.
        self.init_table_index_ref(conn)

        # Close the connection to the database.
        conn.close()
        return

    def init_table_application(self, conn):
        """Create the application table in the user database and insert the
        default values.
        @param  conn    The connection to the database."""
        # If the application table does not exist in the database:
        if not self.check_DB_exist(conn, 'application'):
            # Create the cursor to preform the queries.
            c = conn.cursor()

            # Create the application table with the appropriate fields.
            c.execute("""create table application (
                id integer primary key autoincrement,
                username text collate nocase,
                password text,
                email text collate nocase,
                usergroup integer,
                content text collate nocase,
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

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            # Return false to indicate that the table was not created.
            return False

    def init_table_user(self, conn):
        """Create the user table in the user database and insert the default
        values.
        @param  conn    The connection to the database."""
        # Check whether the user table does not exist in the database.
        if not self.check_DB_exist(conn, 'user'):
            # Create the cursor to preform the queries.
            c = conn.cursor()

            # Create the user table with the appropriate fields. The "id" field
            # denotes the user, not the username.
            c.execute("""create table user (
                id integer primary key autoincrement,
                username text collate nocase,
                password text,
                email text collate nocase,
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
                ?,
                'example@domain.com',
                1,
                0)""", (new('123').hexdigest(),))
            c.execute("""insert into user values (
                NULL,
                'kevin',
                ?,
                'example@domain.com',
                2,
                0)""", (new('kevin').hexdigest(),))

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            # Return false to indicate that the table was not created.
            return False

    def init_table_usergroup(self, conn):
        """Create the user table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Check whether the usergroup table does not exist in the database.
        if not self.check_DB_exist(conn, 'usergroup'):
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

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            # Return false to indicate that the table was not created.
            return False

    def init_table_invitation(self, conn):
        """Create the invitation table in the usergroup database and insert
        the default values.
        @param  conn    The connection to the database."""
        # Check whether the invitation table does not exist in the database.
        if not self.check_DB_exist(conn, 'invitation'):
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

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            # Return false to indicate that the table was not created.
            return False

    def init_table_document(self, conn):
        """Create the document table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Check whether the document table does not exist in the database.
        if not self.check_DB_exist(conn, 'document'):
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

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            # Return false to indicate that the table was not created.
            return False

    def init_table_comment(self, conn):
        """Create the comment table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Check whether the comment table does not exist in the database.
        if not self.check_DB_exist(conn, 'comment'):
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
            c.execute("""insert into comment values (
                NULL, ?, ?, ?, ? )""",
                (0, 0, 'Sample content...', time()))

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            # Return false to indicate that the table was not created.
            return False

    def init_table_complaint(self, conn):
        """Create the complaint table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Check whether the complaint table does not exist in the database.
        if not self.check_DB_exist(conn, 'complaint'):
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
            c.execute("""insert into complaint values (
                NULL,
                ?, ?, ?, ?, ? )""", (0, 0, 'Sample complaint...', time(), 0))

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            # Return false to indicate that the table was not created.
            return False

    def init_table_directory(self, conn):
        """Create the directory table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Check whether the directory table does not exist in the database.
        if not self.check_DB_exist(conn, 'directory'):
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

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            # Return false to indicate that the table was not created.
            return False

    def init_table_member(self, conn):
        """Create the member table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Check whether the member table does not exist in the database.
        if not self.check_DB_exist(conn, 'member'):
            # Create the cursor to preform the queries.
            c = conn.cursor()

            # Create the member table with the appropriate fields.
            c.execute("""create table member (
                id integer primary key autoincrement,
                userid integer,
                docid integer
            )""")

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            # Return false to indicate that the table was not created.
            return False

    def init_table_stop_words(self, conn):
        """Create the stop_words table in the user database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Check whether the user table does not exist in the database.
        if not self.check_DB_exist(conn, 'stop_words'):
            # Create the cursor to preform the queries.
            c = conn.cursor()

            # Create the user table with the appropriate fields. The "id" field
            # denotes the user, not the username.
            c.execute("""create table stop_words (
                id integer primary key autoincrement,
                word text)""")

            # Insert a default words.
            c.execute("insert into stop_words values (NULL, ?)", ("as",))
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

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            # Return false to indicate that the table was not created.
            return False

    def init_table_index_word(self, conn):
        """Create the index table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Check whether the user table does not exist in the database.
        if not self.check_DB_exist(conn, 'index_word'):
            # Create the cursor to preform the queries.
            c = conn.cursor()

            # Create the index_word table with the appropriate fields. The "id"
            # field denotes the directory, not the name field.
            c.execute("""create table index_word (
                id integer primary key autoincrement,
                word text
            )""")

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            # Return false to indicate that the table was not created.
            return False

    def init_table_index_ref(self, conn):
        """Create the index_ref table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Check whether the user table does not exist in the database.
        if not self.check_DB_exist(conn, 'index_ref'):
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

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            # Return false to indicate that the table was not created.
            return False

    def init_table_autocomplete(self, conn):
        """Create the index table in the usergroup database and insert the
        default values.
        @param  conn    The connection to the database."""
        # Create the cursor to preform the queries.
        c = conn.cursor()

        # Check whether the user table does not exist in the database.
        if self.check_DB_exist(conn, 'autocomplete'):
            # Delete the table from the database.
            c.execute("""delete from autocomplete""")
            
        # Create the autocomplete table with the appropriate fields. The "id"
        # field denotes the directory, not the name field.
        c.execute("""create table autocomplete (
            id integer primary key autoincrement,
            word text
        )""")

        # Commit all the changes we have made to the database and close the
        # cursor.
        conn.commit()
        c.close()

        # Return true to indicate that the table was created successfully.
        return True

    def init_table_usrdic(self, userid):
        """Create the userid table in the usrdic database and insert the
        default values.
        @param  conn    The connection to the database."""
        # At this point, the user database must exist, so create a database
        # connection to the file.
        conn = sqlite3.connect('%s/usrdic.db' % self.BASE_DIR)

        # If the table does not exist in the database:
        if not check_DB_exist(conn, '%s' % userid):
            # Create the cursor to preform the queries.
            c = conn.cursor()

            # Create the index_ref table with the appropriate fields. The "id"
            # field denotes the directory, not the name field.
            c.execute("""create table %s (
                id integer primary key autoincrement,
                word text collate nocase
            )""" % userid)

            # Commit all the changes we have made to the database and close the
            # cursor.
            conn.commit()
            c.close()
            conn.close()

            # Return true to indicate that the table was created successfully.
            return True
        # Else the table does already exist in the database:
        else:
            conn.close()
            # Return false to indicate that the table was not created.
            return False

    def print_DB(self, name):
        # At this point, the database must exist, so create a database
        # connection to the file.
        conn = sqlite3.connect('%s/%s.db' % (self.BASE_DIR, name))

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # The query searches the database for all the tables.
        c.execute("""select * from sqlite_master""")

        # Get all the results, if any.
        res = c.fetchall()

        # If any tables exist in the database:
        if res:
            # Make a list of only the table names.
            res = [row[1] for row in res]
            # Remove the master table name from the list.
            res.remove('sqlite_sequence')

            # For each table in the list:
            for table in res:
                print '='*5, table, '='*5
                # Query the current table to all the rows.
                c.execute("""select * from %s""" % table)

                # Get all the results, if any.
                rows = c.fetchall()

                # If there are rows in the table:
                if rows:
                    # For each row in the table:
                    for row in rows:
                        # Print the row.
                        print row

        # Close the cursor to the database and then close the database.
        c.close()
        conn.close()
        return

    def get_table_columns(self, cursor, table, verbose=False):
        # Query the supplied table for its column names.
        cursor.execute("PRAGMA table_info(%s)" % table)

        # Return all the column names found.
        return set( row[1] for row in cursor.fetchall())

    def get_info(self, table, rowid=0, where={}, verbose=False):
        # At this point, the database must exist, so create a database
        # connection to the file. The document database contains a larger
        # percentage of the tables, so assume that the table is in the
        # document database.
        conn = sqlite3.connect(self.BASE_DIR + '/document.db')

        # If the supplied table is not in the document database:
        if not self.check_DB_exist(conn, table):
            # Create a connection to the user database.
            conn = sqlite3.connect(self.BASE_DIR + '/user.db')

            # If the supplied table is not in the user database:
            if not self.check_DB_exist(conn, table):
                # Return the None type, indicating failure.
                return None

        # Set the datbase object to index results by column names.
        conn.row_factory = sqlite3.Row

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # If the search is by rowid of the table:
        if rowid:
            # Query the supplied table for the supplied row.
            c.execute("select * from %s where id=?" % table, (rowid,))

            # Get 1 result, if any.
            res = c.fetchone()

            # Close the cursor to the database and then close the database.
            c.close()
            conn.close()

            # If there is a result, return the result as a dictionary, else
            # return an empty dictionary.
            return dict(res) if res else {}

        # If the search is by other parameters:
        elif where:
            # Generate a list of all valid searchable parameters based on the
            # supplied table.
            valid = self.get_table_columns(c, table, verbose)
            if verbose: print 'Valid Inputs:', valid

            # Find the keys that exist in the supplied dictionary, but not in
            # the list of value keys.
            minus = set(where.keys()) - valid # [ item for item in where.keys() if item not in valid]
            if verbose: print 'Invalid keys:', minus

            # If all the supplied keys are valid:
            if not minus:
                # Generate a query string from the supplied keys.
                query = '=? AND '.join(where.keys()) + '=?'
                if verbose: print 'Query:', query, '\nValues:', where.values()

                # Query the supplied table with the supplied parameters.
                c.execute('select * from %s where %s' % (table, query),
                    where.values())

                # Get all the results, if any.
                res = c.fetchall()

                # Close the cursor to the database and then close the database.
                c.close()
                conn.close()

                # Return all the results as a list of dictionaries, where each
                # dictionary is a row of the result.
                return [dict(row) for row in res]

            # Else at least 1 of the supplied keys are invalid:
            else:
                # Return the None type, indicating failure.
                return None
        # Else no searchable information was supplied:
        else:
            # Return the None type, indicating failure.
            return None

    def update_info(self, table, update={}, where={}, verbose=False):
        # At this point, the database must exist, so create a database
        # connection to the file. The document database contains a larger
        # percentage of the tables, so assume that the table is in the
        # document database.
        conn = sqlite3.connect(self.BASE_DIR + '/document.db')

        # If the supplied table is not in the document database:
        if not self.check_DB_exist(conn, table):
            # Create a connection to the user database.
            conn = sqlite3.connect(self.BASE_DIR + '/user.db')

            # If the supplied table is not in the user database:
            if not self.check_DB_exist(conn, table):
                # Return the None type, indicating failure.
                return None

        # Set the datbase object to index results by column names.
        conn.row_factory = sqlite3.Row

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # If update and where parameters were supplied:
        if update and where:
            # Generate a list of all valid searchable and updatable parameters
            # based on the supplied table.
            valid = self.get_table_columns(c, table, verbose)
            if verbose: print 'Valid Inputs:', valid

            # Find the keys that exist in the supplied searching dictionary, but
            # not in the list of valid value keys.
            minus = set(where.keys()) - valid # [ item for item in where.keys() if item not in valid]
            # Extend the list of invalid keys to include the keys that exist in
            # the supplied update dictionary, but not in the valid key values.
            minus.extend(set(update.keys()) - valid) # [ item for item in update.keys() if item not in valid])
            if verbose: print 'Invalid keys:', minus

            # If all the supplied keys are valid:
            if not minus:
                # Generate a update string from the supplied update keys.
                update_str = '=? AND '.join(update.keys()) + '=?'
                if verbose:
                    print 'Update:', update_str, '\nValues:', update.values()

                # Generate a query string from the supplied where keys.
                where_str = '=? AND '.join(where.keys()) + '=?'
                if verbose:
                    print 'Query:', where_str, '\nValues:', where.values()

                # Query the supplied table with the supplied parameters.
                c.execute('update %s set %s where %s' %
                    (table, update_str, where_str),
                    update.values().extend(where.values()))

                # Commit the changes.
                conn.commit()

                # Close the cursor to the database and then close the database.
                c.close()
                conn.close()

                # Return true to denote success.
                return True

        # Else no update and/or where parameters were supplied.
        else:
            # Return the None-Type to indicate failure.
            return None

    def insert_info(self, table, insert={}, verbose=False):
        # At this point, the database must exist, so create a database
        # connection to the file. The document database contains a larger
        # percentage of the tables, so assume that the table is in the
        # document database.
        conn = sqlite3.connect(self.BASE_DIR + '/document.db')

        # If the supplied table is not in the document database:
        if not self.check_DB_exist(conn, table):
            # Create a connection to the user database.
            conn = sqlite3.connect(self.BASE_DIR + '/user.db')

            # If the supplied table is not in the user database:
            if not self.check_DB_exist(conn, table):
                # Return the None type, indicating failure.
                return None

        # Set the datbase object to index results by column names.
        conn.row_factory = sqlite3.Row

        # Create the cursor to preform the queries.
        c = conn.cursor()

        # If insert parameters were supplied:
        if insert:
            # Generate a list of all valid insertion parameters based on the
            # supplied table.
            valid = self.get_table_columns(c, table, verbose)
            if verbose: print 'Valid Inputs:', valid

            # Find the keys that exist in the supplied searching dictionary, but
            # not in the list of valid value keys.
            minus = set(insert.keys()) - valid # [ item for item in insert.keys() if item not in valid]
            if verbose: print 'Invalid keys:', minus

            # If all the supplied keys are valid:
            if not minus:
                # Check for the supplied parameters in the table.
                res = self.get_info(table, where=insert, verbose=verbose)

                # If the supplied paramaters are not in the table:
                if not res:
                    # Generate a fields string from the supplied update keys.
                    fields = ', '.join(insert.keys())

                    # Generate a query string from the supplied update keys.
                    query = ''.join(['?, ' for i in insert.keys()])[:-2]

                    if verbose:
                        print 'Fields:', fields, '\nKeys:', insert.keys()
                        print 'Query:', query, '\nValues:', insert.values()
                        print 'insert into %s (%s) values (%s)' % (table, fields, query), insert.values()

                    # Query the supplied table with the supplied parameters.
                    c.execute('insert into %s (%s) values (%s)' %
                        (table, fields, query), insert.values())

                    # Commit the changes.
                    conn.commit()

                    # Close the cursor to the database and then close the
                    # database.
                    c.close()
                    conn.close()

                    # Return true to denote success.
                    return True
                # Else the supplied paramaters are in the table:
                else:
                    # Return false to denote failure.
                    return False

        # Else no insertion parameters were supplied.
        else:
            # Return the None-Type to indicate failure.
            return None

if __name__ == "__main__":
    verbose = False
    dbm = Database()
    # Insert User.
    dbm.insert_info('user', insert={
        'username': 'Gary',
        'password': new('boss').hexdigest(),
        'email': 'GOak@pokemon.com',
        'usergroup': 2,
        'infraction': 0}, verbose=verbose)
    dbm.print_DB('user')

    dbm.insert_info('directory', insert={
        'name': 'Oak',
        'parent_dir': 1}, verbose=verbose)
    dbm.print_DB('document')
