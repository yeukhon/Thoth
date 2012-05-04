from Tkinter import *
from sqlite3 import connect
from user import User
from application import ApplicationManager


class App_Viewer_Window:
    BASE_DIR = 'dbs'

    def __init__(self, master, parent, user):
        self.user = user
        self.parent = parent
        self.manage_App = ApplicationManager(user)

        self.frame = Frame(master, relief=FLAT)

        self.init_frame_pending()
        self.frame_pending.grid()

        self.frame_quit = Button(
            self.frame,
            text='Home',
            command=self.handler_goto_homepage)
        self.frame_quit.grid()

        return

    def init_frame_pending(self):
        self.frame_pending = LabelFrame(
            self.frame,
            text='Pending Applications')
        self.frame_pending.columnconfigure(0, weight=2)
        self.frame_pending.columnconfigure(1, weight=2)
        self.frame_pending.columnconfigure(2, weight=22)
        self.frame_pending.columnconfigure(3, weight=2)
        self.frame_pending.columnconfigure(4, weight=1)
        self.frame_pending.columnconfigure(5, weight=1)

        self.frame_pending_header_username = Label(
            self.frame_pending,
            text='Username')
        self.frame_pending_header_username.grid(row=0, column=0)

        self.frame_pending_header_email = Label(
            self.frame_pending,
            text='Email')
        self.frame_pending_header_email.grid(row=0, column=1)

        self.frame_pending_header_content = Label(
            self.frame_pending,
            text='Content')
        self.frame_pending_header_content.grid(row=0, column=2)

        self.frame_pending_header_time = Label(
            self.frame_pending,
            text='Time')
        self.frame_pending_header_time.grid(row=0, column=3)

        self.frame_pending_header_action = Label(
            self.frame_pending,
            text='Action')
        self.frame_pending_header_action.grid(row=0, column=4, columnspan=2)

        res = [{'username': 'my_name', 'email': 'g@g.com', 'time': 'Dec 06, 2011', 'content': 'abcdef'}]#self.manage_App.view_applications_pending()
        start = 1
        self.pending_invitations = []
        for row in res:
            self.pending_invitations.append([
                Label(
                    self.frame_pending,
                    text=row['username']
                ),
                Label(
                    self.frame_pending,
                    text=row['email']
                ),
                Label(
                    self.frame_pending,
                    text=row['content']
                ),
                Label(
                    self.frame_pending,
                    text=row['time']
                ),
                Button(
                    self.frame_pending,
                    text='Accept'
                ),
                Button(
                    self.frame_pending,
                    text='Deny'
                )
            ])
            self.pending_invitations[-1][0].grid(row=start, column=0)
            self.pending_invitations[-1][1].grid(row=start, column=1)
            self.pending_invitations[-1][2].grid(row=start, column=2)
            self.pending_invitations[-1][3].grid(row=start, column=3)
            self.pending_invitations[-1][4].grid(row=start, column=4)
            self.pending_invitations[-1][5].grid(row=start, column=5)
            start += 1

        return

    def handler_goto_homepage(self):
        self.frame.grid_remove()
        self.parent.frame.grid()
        return


class App_Form_Window:
    BASE_DIR = 'dbs'

    def __init__(self, master, parent, user):
        self.user = user
        self.parent = parent
        self.manage_App = ApplicationManager(user)

        self.frame = Frame(master, relief=FLAT)

        self.init_frame_form()
        self.frame_form.grid()

        self.frame_quit = Button(
            self.frame,
            text='Home',
            command=self.handler_goto_homepage)
        self.frame_quit.grid()

        return

    def init_frame_form(self):
        self.frame_form = LabelFrame(
            self.frame,
            text='Apply To The System')
        self.frame_form.columnconfigure(0, weight=2)
        self.frame_form.columnconfigure(1, weight=2)
        self.frame_form.columnconfigure(2, weight=22)
        self.frame_form.columnconfigure(3, weight=2)
        self.frame_form.columnconfigure(4, weight=1)
        self.frame_form.columnconfigure(5, weight=1)

        place = 0
        self.form_username = StringVar()
        self.frame_form_label_username = Label(
            self.frame_form,
            text='Username:')
        self.frame_form_label_username.grid(row=place, column=0)
        self.frame_form_username = Entry(
            self.frame_form,
            textvariable=self.form_username)
        self.frame_form_username.grid(row=place, column=1)

        place += 1
        self.form_password = StringVar()
        self.frame_form_label_password = Label(
            self.frame_form,
            text='Password:')
        self.frame_form_label_password.grid(row=place, column=0)
        self.frame_form_password = Entry(
            self.frame_form,
            textvariable=self.form_password,
            show='*')
        self.frame_form_password.grid(row=place, column=1)

        place += 1
        self.form_password2 = StringVar()
        self.frame_form_label_password2 = Label(
            self.frame_form,
            text='Confirm Password:')
        self.frame_form_label_password2.grid(row=place, column=0)
        self.frame_form_password2 = Entry(
            self.frame_form,
            textvariable=self.form_password2,
            show='*')
        self.frame_form_password2.grid(row=place, column=1)

        place += 1
        self.form_email = StringVar()
        self.frame_form_label_email = Label(
            self.frame_form,
            text='Email:')
        self.frame_form_label_email.grid(row=place, column=0)
        self.frame_form_email = Entry(
            self.frame_form,
            textvariable=self.form_email)
        self.frame_form_email.grid(row=place, column=1)

        place += 1
        self.form_content = StringVar()
        self.frame_form_label_content = Label(
            self.frame_form,
            text='Reason:')
        self.frame_form_label_content.grid(row=place, column=0)
        self.frame_form_content = Text(
            self.frame_form,
            height=5,
            width=23,
            wrap=WORD)
        self.frame_form_content.insert(
            END,
            'What is your pourpose in joining the system?')
        self.frame_form_content.grid(row=place, column=1)

        place += 1
        self.frame_form_submit = Button(
            self.frame_form,
            text='Submit',
            command=self.handler_submit_form)
        self.frame_form_submit.grid(row=place, columnspan=2)

        return

    def handler_submit_form(self):
        res = self.user.manage_User.get_user_id(self.form_username.get())
        if res[0]:
            self.frame_form_username.config(bg='red')
        else:
            self.frame_form_username.config(bg='light gray')

        if self.form_password.get() != self.form_password2.get():
            self.frame_form_password.config(bg='red')
            self.frame_form_password2.config(bg='red')
        else:
            self.frame_form_password.config(bg='light gray')
            self.frame_form_password2.config(bg='light gray')

        return

    def handler_goto_homepage(self):
        self.frame.grid_remove()
        self.parent.frame.grid()
        return


if __name__ == "__main__":
    root = Tk()
    user = User(2)
    tb = App_Viewer_Window(root, 0, user)
#    tb = App_Form_Window(root, 0, user)
    tb.frame.pack(fill='both', expand=1)
    mainloop()
