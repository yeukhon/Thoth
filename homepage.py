from Tkinter  import *
from user import User
import tkMessageBox
from invitation_win import Invitation_Viewer_Window
from application_win import App_Viewer_Window
from login_win import Login_Window
from textbox import TextBox
from document import Document, DocumentManager


class Homepage:
    BASE_DIR = 'dbs'

    def __init__(self, master, user):
        self.user = user
        self.user.manage_DB.check()
        self.manage_Docs = DocumentManager(self.user.manage_DB)

        # Child Windows:
        self.window_login = Login_Window(master, self, self.user)
        self.window_editor = TextBox(master, self)
        self.window_invitations = Invitation_Viewer_Window(
            master, self, self.user)
        self.window_applications = App_Viewer_Window(master, self, self.user)

        self.directory = {'name': '', 'parent_dir': '1'}
        self.directory_contents = []

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

        self.frame_dir.grid(row=0, column=0, sticky=N + E + S + W, padx="20px", pady="10px")
        self.frame_create.grid(row=1, column=0, sticky=N + E + S + W, padx="20px", pady="10px")
        self.frame_cpanel.grid(row=0, column=1, rowspan=2, sticky=N + E + S + W, padx="20px", pady="10px")

        return

    def init_frame_directory(self):
        # Left Side Frame.
        self.frame_dir = LabelFrame(
            self.frame,
            text='Directory Files:')
        self.frame_dir.columnconfigure(0, weight=30)
        self.frame_dir.columnconfigure(1, weight=1)

        # Displays the current directory
        self.frame_directory_label = Label(
            self.frame_dir,
            text=self.directory['name'] + '/',
            fg='#ffa500', bg='#333')
        self.frame_directory_label.grid(
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
            text=self.user.info['username'],
            fg='#ffa500', bg='#333')
        self.frame_cpanel_user.grid(sticky=N + E + S + W)

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
        # Create the menubar that will hold all the menus and thier items.
        self.menubar = Menu(self.frame)

        # File Pulldown menu, contains "Open", "Save", and "Exit" options.
        self.filemenu = Menu(self.menubar, tearoff=0)
	self.loginmenu = Menu(self.menubar, tearoff=0)

	if self.user.info['usergroup'] == 4:
            self.loginmenu.add_command(label="Login", command=self.handler_view_login)
            self.loginmenu.add_command(label="Register", command=self.handler_view_register)
	    self.menubar.add_cascade(label="Login/Register", menu=self.loginmenu)
            #self.filemenu.add_separator()
	elif self.user.info['usergroup'] <= 2:	# superuser or normal user
	    self.loginmenu.add_command(label="Logout", command=self.handler_view_logout)
	    self.menubar.add_cascade(label="My Account", menu=self.loginmenu)

        self.filemenu.add_command(label="Quit", command=self.file_exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

	self.helpmenu = Menu(self.menubar, tearoff=0)
	self.helpmenu.add_command(label="Get Help", command=self.show_help)
	self.helpmenu.add_command(label="About", command=self.show_about)
	self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.top["menu"] = self.menubar
        return

    def update_directory(self, directoryid):
        # Get the information for the supplied directory.
        self.directory = self.user.manage_DB.get_directory_info(directoryid)

        # Get a list of the directories in the supplied directory.
        self.directory_dir = self.user.manage_Dir.get_directory_directories(
            directoryid)
        # Get a list of the documents in the supplied directory.
        self.directory_doc = self.manage_Docs.get_directory_documents(
            directoryid)

        # Remove the labels from the previous directory from the grid.
        for label in self.directory_contents:
            label[0].grid_remove()
            label[1].grid_remove()
        # Reset the directory contents list to empty.
        self.directory_contents = []

        # Display the current directory.
        self.frame_directory_label.configure(
            text=self.directory['name'] + '/')

        # Contents of the directory start on row 2.
        start = 2
        for row in self.directory_dir:
            # Each entry of the directory_contents list will be the entire row
            # of the grid. Each row is composed of a Label for that directory
            # and a Button to move into that directory.
            self.directory_contents.append([
                Label(
                    self.frame_dir,
                    fg='#0000ff',
                    text=row['name'] + '/'),
                Button(
                    self.frame_dir,
                    text='View',
                    relief=RAISED,
                    command=lambda i=row['id']: self.update_directory(i))])
            # Add the Label to the row specified by 'start', column 0
            self.directory_contents[-1][0].grid(
                row=start, column=0, sticky=N + E + S + W)
            # Add the Button to the row specified by 'start', column 1
            self.directory_contents[-1][1].grid(
                row=start, column=1, sticky=N + E + S + W)
            # Increment 'start'.
            start += 1

        for row in self.directory_doc:
            # Each entry of the directory_contents list will be the entire row
            # of the grid. Each row is composed of a Label for that document
            # and a Button see the information about the document.
            self.directory_contents.append([
                Label(
                    self.frame_dir,
                    fg='#3399FF',
                    text=row['name']),
                Button(self.frame_dir,
                    text='Info',
                    relief=RAISED,
                    command=lambda i=row['id']: self.open_document(i))])
            # Add the Label to the row specified by 'start', column 0
            self.directory_contents[-1][0].grid(
                row=start, column=0, sticky=N + E + S + W)
            # Add the Button to the row specified by 'start', column 1
            self.directory_contents[-1][1].grid(
                row=start, column=1, sticky=N + E + S + W)
            # Increment 'start'.
            start += 1

        # Get the logical path for the supplied directory.
        path_logical = self.user.manage_Dir.get_directory_path(
            self.directory['id'])[0]
        # Set the Label to create a directory at the logical path.
        self.frame_create_banner_dir.config(
            text='Directory @ ' + path_logical + ':')
        # Set the Label to create a document at the logical path.
        self.frame_create_banner_doc.config(
            text='Document @ ' + path_logical + ':')
        return

    def open_document(self, docid):
        self.window_editor.initialize(self.user, Document(docid))
        self.frame.grid_remove()
        self.window_editor.frame.grid()
        return

    def handler_directory_up(self):
        # The current directory has a parent_dir.
        if self.directory['parent_dir']:
            # Update the Label to show the contents of parent_dir.
            self.update_directory(self.directory['parent_dir'])
        return

    def handler_create_directory(self):
        # The user is of the 'Regular Users' or 'Super User' usergroup.
        if self.user.info['usergroup'] <= 2:
            # Get the name of the directory the user wants to create.
            name = self.entry_dirname.get()
            # Insert a directory in the dB at the current directory.
            res = self.user.manage_DB.insert_directory(
                name, self.directory['id'])

            # The directory does not already exist in the dB.
            if res:
                # Get the 'id' of the newly created directory.
                newid = self.user.manage_DB.get_directory_info(
                    name=name, parent_dir=self.directory['id'])['id']
                # Create the directory.
                res = self.user.manage_Dir.create_directory(newid)

                # The directory does not already exist on the file system.
                if res:
                    # Delete the directory name from the creation box.
                    self.entry_dirname.delete(0, len(name))
                    # Update the display to show the newly created directory.
                    self.update_directory(self.directory['id'])
                # The directory already exist on the file system.
                else:
                    # Show the appropriate error message.
                    tkMessageBox.showerror(
                        'Error Creating Directory!',
                        'Directory "' + name +
                        '" already exist on the file system!')
            # The directory already exist in the dB.
            else:
                # Show the appropriate error message.
                tkMessageBox.showerror(
                    'Error Creating Directory!',
                    'Directory "' + name +
                    '" already exist in the database!')
        # User is of the 'Suspended' usergroup.
        elif self.user.info['usergroup'] == 3:
            # Show the appropriate error message.
            tkMessageBox.showerror(
                'Insufficient Privileges',
                'Your account has been suspended!')
        # User is of the 'Visitor' usergroup.
        else:
            # Show the appropriate error message.
            tkMessageBox.showerror(
                'Insufficient Privileges',
                'You must login before you can preform this action!')

        return

    def handler_create_document(self):
        # The user is of the 'Regular Users' or 'Super User' usergroup.
        if self.user.info['usergroup'] <= 2:
            # Get the name of the document the user wants to create.
            name = self.entry_docname.get()
            # Insert a document in the dB at the current directory.
            res = self.user.manage_DB.insert_document(
                name, self.directory['id'], self.user.info['id'], 0, 0, 0, 0)

            # The document does not already exist in the dB.
            if res:
                # Get the 'id' of the newly created document.
                newid = self.user.manage_DB.get_document_info(
                    name=name, parent_dir=self.directory['id'])['id']
                # Create the document.
                res = self.manage_Docs.create_document(
                    newid, self.directory['id'])

                # The document does not already exist on the file system.
                if res:
                    # Delete the document name from the creation box.
                    self.entry_docname.delete(0, len(name))
                    # Update the display to show the newly created document.
                    self.update_directory(self.directory['id'])
                # The document already exist on the file system.
                else:
                    # Show the appropriate error message.
                    tkMessageBox.showerror(
                        'Error Creating Document!',
                        'Document "' + name +
                        '" already exist on the file system!')
            # The document already exist in the dB.
            else:
                # Show the appropriate error message.
                tkMessageBox.showerror(
                    'Error Creating Document!',
                    'Document "' + name +
                    '" already exist in the database!')
        # User is of the 'Suspended' usergroup.
        elif self.user.info['usergroup'] == 3:
            # Show the appropriate error message.
            tkMessageBox.showerror(
                'Insufficient Privileges',
                'Your account has been suspended!')
        # User is of the 'Visitor' usergroup.
        else:
            # Show the appropriate error message.
            tkMessageBox.showerror(
                'Insufficient Privileges',
                'You must login before you can preform this action!')

        return

    def handler_view_invitations(self):
        self.frame.grid_remove()
        self.window_invitations.frame.grid()
        return

    def handler_view_login(self):
        #self.top["menu"] = 0
        #self.frame.grid_remove()
	#self.init_menus()
        self.window_login.frame.grid()
        return

    def handler_view_register(self):
	pass

    def handler_view_logout(self):
	pass

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
