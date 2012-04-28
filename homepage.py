from Tkinter  import *
from user import User
import tkMessageBox
from invitation_win import Invitation_Viewer_Window
from application_win import App_Viewer_Window
from login_win import Login_Window
from textbox import TextBox
from document import Document


class Homepage:
    BASE_DIR = 'dbs'

    def __init__(self, master, user):
        self.user = user
        self.user.manage_DB.check()

        # Child Windows:
        self.window_login = Login_Window(master, self, self.user)
        self.window_editor = TextBox(master)
        self.window_invitations = Invitation_Viewer_Window(
            master, self, self.user)
        self.window_applications = App_Viewer_Window(master, self, self.user)

        self.curr_directory = {'name': '', 'parent_dir': '1'}
        self.curr_directory_contents = []

        self.font = ("Helvetica", "20", "normal")

        self.top = master.winfo_toplevel()
        self.init_frame(master)
        self.init_menus()
        return

    def init_frame(self, master):
        self.frame = Frame(master, relief=FLAT)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.init_frame_directory()
        self.init_frame_create()
        self.init_frame_cpanel()
        self.update_directory(1)

        self.frame_dir.grid(row=0, column=0, sticky=N + E + S + W)
        self.frame_create.grid(row=1, column=0, sticky=N + E + S + W)
        self.frame_cpanel.grid(row=0, column=1, rowspan=2,
            sticky=N + E + S + W)

        return

    def init_frame_directory(self):
        # Left Side Frame.
        self.frame_dir = LabelFrame(
            self.frame,
            text='Directory Files:')
        self.frame_dir.columnconfigure(0, weight=30)
        self.frame_dir.columnconfigure(1, weight=1)

        # Displays the current directory
        self.frame_dir_ctrl_label = Label(
            self.frame_dir,
            text=self.curr_directory['name'] + '/',
            fg='#ffa500')
        self.frame_dir_ctrl_label.grid(
            row=1, column=0, sticky=N + E + S + W)

        # Button to go up a directory
        self.frame_dir_ctrl_up = Button(
            self.frame_dir,
            text='Up',
            width=4,
            padx=1,
            relief=RAISED,
            command=self.handler_directory_up)
        self.frame_dir_ctrl_up.grid(row=1, column=1, sticky=N + E + S + W)

        return

    def init_frame_create(self):
        # Create file and directory frame
        self.frame_create = LabelFrame(
            self.frame,
            text='Creation:')
        self.frame_create.columnconfigure(0, weight=30)
        self.frame_create.columnconfigure(1, weight=1)

        # Create Directory
        self.frame_create_banner_dir = Label(
            self.frame_create)
        self.frame_create_banner_dir.grid(
            row=0, column=0, columnspan=2, sticky=N + S + W)

        self.entry_dirname = Entry(self.frame_create)
        self.entry_dirname.grid(row=1, column=0, sticky=N + E + S + W)
        self.button_dirname = Button(
            self.frame_create,
            text='Create',
            width=5,
            padx=1,
            relief=RAISED,
            command=self.handler_create_directory)
        self.button_dirname.grid(row=1, column=1, sticky=N + E + S + W)

        # Create Document
        self.frame_create_banner_doc = Label(
            self.frame_create)
        self.frame_create_banner_doc.grid(
            row=2, column=0, columnspan=2, sticky=N + S + W)

        self.entry_docname = Entry(self.frame_create)
        self.entry_docname.grid(row=3, column=0, sticky=N + E + S + W)
        self.button_docname = Button(
            self.frame_create,
            text='Create',
            width=5,
            padx=1,
            relief=RAISED,
            command=self.handler_create_document)
        self.button_docname.grid(row=3, column=1, sticky=N + E + S + W)

        return

    def init_frame_cpanel(self):
        self.frame_cpanel = LabelFrame(self.frame, text='Control Panel:')
        self.frame_cpanel.columnconfigure(0, weight=1)

        self.frame_cpanel_user = Label(
            self.frame_cpanel,
            text=self.user.info['username'])
        self.frame_cpanel_user.grid()

        # View Your Documents Button
        self.frame_cpanel_ownerdocs = Button(
            self.frame_cpanel,
            text='Documents',
            width=11,
            relief=RAISED)
        self.frame_cpanel_ownerdocs.grid()

        # View Invitations Button
        self.frame_cpanel_invitations = Button(
            self.frame_cpanel,
            text='Invitations',
            width=11,
            relief=RAISED,
            command=self.handler_view_invitations)
        self.frame_cpanel_invitations.grid()

        # Search Button
        self.frame_cpanel_search = Button(
            self.frame_cpanel,
            text='Search',
            width=11,
            relief=RAISED)
        self.frame_cpanel_search.grid()

        # View Complaints Button
        self.frame_cpanel_complaints = Button(
            self.frame_cpanel,
            text='Complaints',
            width=11,
            relief=RAISED)
        self.frame_cpanel_complaints.grid()

        return

    def init_menus(self):
        """Initializes the FILE, EDIT, and ABOUT menus."""

        # Create the menubar that will hold all the menus and thier items.
        self.menubar = Menu(self.frame)

        # File Pulldown menu, contains "Open", "Save", and "Exit" options.
        self.filemenu = Menu(self.menubar, tearoff=0)
        if self.user.info['usergroup'] == 4:
            self.filemenu.add_command(label="Login",
            command=self.handler_view_login)
            self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.file_exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.top["menu"] = self.menubar
        return

    def update_directory(self, dirid):
        self.curr_directory = self.user.manage_DB.get_directory_info(dirid)
        self.curr_directory_contents_dir = self.user.manage_Dir.get_dir_dir(
            dirid)
        self.curr_directory_contents_doc = self.user.manage_Docs.get_directory_documents(dirid)

        # Remove the old items from the list.
        for label in self.curr_directory_contents:
            label[0].grid_remove()
            label[1].grid_remove()
        self.curr_directory_contents = []

        self.frame_dir_ctrl_label.configure(
            text=self.curr_directory['name'] + '/')
        start = 2
        for row in self.curr_directory_contents_dir:
            self.curr_directory_contents.append([
                Label(
                    self.frame_dir,
                    fg='#0000ff',
                    text=row['name'] + '/'),
                Button(
                    self.frame_dir,
                    text='View',
                    relief=RAISED,
                    command=lambda i=row['id']: self.update_directory(i))])
            self.curr_directory_contents[-1][0].grid(
                row=start, column=0, sticky=N + E + S + W)
            self.curr_directory_contents[-1][1].grid(
                row=start, column=1, sticky=N + E + S + W)
            start += 1

        for row in self.curr_directory_contents_doc:
            self.curr_directory_contents.append([
                Label(
                    self.frame_dir,
                    fg='#3399FF',
                    text=row['name']),
                Button(self.frame_dir,
                    text='Info',
                    relief=RAISED,
                    command=lambda i=row['id']: self.open_document(i))])
            self.curr_directory_contents[-1][0].grid(
                row=start, column=0, sticky=N + E + S + W)
            self.curr_directory_contents[-1][1].grid(
                row=start, column=1, sticky=N + E + S + W)
            start += 1

        curr_dir = self.user.manage_Dir.get_dir_path(
            self.curr_directory['id'])
        self.frame_create_banner_dir.config(
            text='Directory @ ' + curr_dir + ':')
        self.frame_create_banner_doc.config(
            text='Document @ ' + curr_dir + ':')
        return

    def open_document(self, docid):
        self.window_editor.initialize(self.user, Document(docid))
        self.frame.grid_remove()
        self.window_editor.frame.grid()
        return

    def handler_directory_up(self):
        if self.curr_directory['parent_dir'] != 0:
            self.update_directory(self.curr_directory['parent_dir'])
        return

    def handler_create_directory(self):
        res_add = self.user.manage_Dir.add_directory(
            self.entry_dirname.get(), self.curr_directory['id'])
        res_cre = 1
        if res_add[0]:
            res_cre = self.user.manage_Dir.create_directory(
                res_add[1], self.curr_directory['id'])
            self.update_directory(self.curr_directory['id'])
            self.entry_dirname.delete(0, len(self.entry_dirname.get()))

        if not res_add[0] or not res_cre:
            tkMessageBox.showerror(
                'Error Creating Directory!',
                'Directory "' + self.entry_dirname.get() + '" already exist!')

        return

    def handler_create_document(self):
        res_add = self.user.manage_Docs.add_document(
            self.entry_docname.get(),
            self.curr_directory['id'],
            self.user.info['id'],
            0)
        res_cre = [1]
        if res_add[0]:
            self.user.manage_Docs.create_document(
                res_add[1], self.curr_directory['id'])
            self.update_directory(self.curr_directory['id'])
            self.entry_docname.delete(0, len(self.entry_docname.get()))

        if not res_add[0] or not res_cre[0]:
            tkMessageBox.showerror(
                'Error Creating Document!',
                'Document "' + self.entry_docname.get() + '" already exist!')

        return

    def handler_view_invitations(self):
        self.frame.grid_remove()
        self.window_invitations.frame.grid()
        return

    def handler_view_login(self):
        self.top["menu"] = 0
        self.frame.grid_remove()
        self.window_login.frame.grid()
        return

    def file_exit(self):
        """Clean-up before exiting a file."""

        self.quit()
        return

if __name__ == "__main__":
    root = Tk()
    user = User(2)
    tb = Homepage(root, user)
    tb.frame.pack(fill='both', expand=1)
    mainloop()
