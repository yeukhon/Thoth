from Tkinter import *
from sqlite3 import connect
from user import User
from md5 import new

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

    def user_login(self, event):
        res = self.user.manage_User.user_in_DB(
            self.username.get(), self.password.get())

        if res[0]:
            self.parent.user.update_user(res[1])
            self.handler_goto_homepage()
        else:
            self.password.set('')
        return

    def handler_goto_homepage(self):
        self.frame.grid_remove()
        self.parent.frame.grid()
        return
