from Tkinter import *
from sqlite3 import connect
from user import User
from md5 import new
import tkMessageBox

class Login_Window:
    BASE_DIR = 'dbs'

    def __init__(self, master, parent, user):
        self.user = user
        self.parent = parent

        self.frame = Frame(master, relief=FLAT)

        self.init_login()
        self.frame_login.grid()

        self.frame_quit = Button(
            self.frame,
            text='Home',
            command=self.handler_goto_homepage)
        self.frame_quit.grid()

        return

    def init_login(self):
        self.frame_login = Frame(self.frame)

        self.username = StringVar()
        self.label_username = Label(self.frame_login, text="Username:")
        self.label_username.grid(row=0, column=0)
        self.entry_username = Entry(
            self.frame_login,
            textvariable=self.username)
        self.entry_username.grid(row=0, column=1)

        self.password = StringVar()
        self.label_password = Label(self.frame_login, text="Password:")
        self.label_password.grid(row=1, column=0)
        self.entry_password = Entry(
            self.frame_login,
            textvariable=self.password,
            show="*")
        self.entry_password.grid(row=1, column=1)

        self.entry_password.bind("<KeyPress-Return>", self.user_login)

        self.button_login = Button(
            self.frame_login,
            text="Login",
            command=self.user_login)
        self.button_login.grid(row=2, columnspan=2, sticky=W+E)

        self.frame_login.grid(row=0)
        return

    def user_login(self, event=0):
        # Get the username the user typed.
        name = self.username.get()
        # Get the password the user typed and md5 it.
        password = new(self.password.get()).hexdigest()

        # Get the information for the supplied username.
        res = self.user.manage.manage_DB.get_info('user', where={'username': name, 'password': password})

        # The supplied username is in the database.
        if res:
            res = res[-1]
            # The supplied password matches the password in the database.
            if res['password'] == password:
                # Update the User instance with the new user information.
                self.parent.user.update_user(res['id'])
                self.parent.frame_cpanel_user.config(text=res['username'])
                # Display the homepage.
                tkMessageBox.showinfo('Authenticated', 'Welcome back! You are logged in as %s.' % res['username'])
                self.handler_goto_homepage()
            # The supplied password does not match the password in the database.
            else:
                # Reset the password field.
                self.password.set('')
        # The supplied username is not in the database.
        else:
            # Reset the username and password field.
            self.username.set('')
            self.password.set('')
            tkMessageBox.showerror('Login Failed', 'Authentication failed. Please try again.')
        return

    def handler_goto_homepage(self):
        self.frame.grid_remove()
        self.parent.frame.grid()
	print dir(self.parent.menubar)
	print self.parent.menubar.keys()
	self.parent.menubar.destroy()
	self.parent.init_menus()
        return
