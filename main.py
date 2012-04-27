from Tkinter import *
from user import *
from textbox import *
from homepage import Homepage


class TEditor(Frame):

    def __init__(self, master=None):
        self.textbox_max_row = 20
        self.textbox_max_col = 50
        self.font = ("Helvetica", "12", "normal")

        Frame.__init__(self, master)
        self.grid()

        self.master.title("TEditor")


#        self.init_menus()
#        self.init_textbox()

        self.user = User(1)
        self.main_GUI = Homepage(self, self.user)
        self.main_GUI.frame.grid(row=0, column=0, sticky=N+E+S+W)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        return

    def init_menus(self):
        """Initializes the FILE, EDIT, and ABOUT menus."""

        # Create the menubar that will hold all the menus and thier items.
        self.menubar = Menu(self)

        # File Pulldown menu, contains "Open", "Save", and "Exit" options.
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.file_open)
        self.filemenu.add_command(label="Save", command=self.file_save)
        self.filemenu.add_command(label="Save As", command=self.file_saveAs)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.file_exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Edit Pulldown menu, contains "Cut", "Copy", and "Paste"
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Cut", command=self.edit_cut)
        self.editmenu.add_command(label="Copy", command=self.edit_copy)
        self.editmenu.add_command(label="Paste", command=self.edit_paste)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Bold", command=self.edit_bold)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        # Help Pulldown menu, contains "About"
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.help_about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)
        return

    def init_textbox(self):
        """Initializes the textbox."""
        self.editor = TextBox(self)
        self.editor.frame.pack(fill='both', expand=1)

        return

    def init_login(self):
        self.frame_login = Frame(self)

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

    def file_open(self):
        """Open a file."""
        print "TODO: Write the open file function!"
        return

    def file_save(self):
        """Save a file."""
        print "TODO: Write the save file function!"
        return

    def file_saveAs(self):
        """Save as a new file."""
        print "TODO: Write the save as file function!"
        return

    def file_exit(self):
        """Clean-up before exiting a file."""
        print "TODO: Write the exit file function!"

        self.quit()
        return

    def edit_cut(self):
        """Cut text selection."""
        print "TODO: Write the cut selected text function!"
        return

    def edit_copy(self):
        """Copy text selection."""
        print "TODO: Write the copy selected text function!"
        return

    def edit_paste(self):
        """Paste text selection."""
        print "TODO: Write the paste selected text function!"
        return

    def edit_bold(self):
        """Bold text selection."""
        print "TODO: Write the bold selected text function!"
        return

    def help_about(self):
        """About dialog."""
        print "TODO: Write the about function!"
        return

    def user_login(self, e):
        """Process the user's login information. Sanitation and
        Validation."""
        print "TODO: Write the login function!"
        self.user_manager = UserManager()
        if self.user_manager.user_in_DB(self.username.get(),
            self.password.get()):
            self.frame_login.grid_remove()
            self.init_menus()
            self.init_textbox()
        else:
            print "User not found!"

        return

if __name__ == "__main__":
    app = TEditor()
    app.master.title("TEditor")
    app.mainloop()
