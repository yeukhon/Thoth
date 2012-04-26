from Tkinter import *
import os
from sqlite3 import connect
import re


class TextBox():
    BASE_DIR = "dbs"

    def __init__(self, master):
        # Time interval at whic we want the line numbers to update.
        self.update_interval = 300

        # This frame will be derived from the frame that is passed to it and will
        # contains three elements, a Text widget for the line numbers, a Text
        # widget for the content, and a vertical scrollbar.
        self.frame = Frame(master, relief=FLAT)

        # The variable that will hold the line numbers. The line numbers are in
        # essence just a string that will be the body of a Text widget.
        self.str_ln = ""

        # The line numbers will be held in a Text widget that is disabled, i.e
        # the users cannnot edit its contents.
        self.text_ln = Text(self.frame, state='disabled', width=1, padx=4,
            background= 'lightgrey', foreground='magenta', relief=FLAT)
        self.text_ln.pack(side=LEFT, fill='y')

        # The Text widget that will contain the content.
        self.str_content = ""
        self.text_content = Text(self.frame, undo=True, bg='#333', fg='#FFF',
            insertbackground='#FFF', selectbackground='#3399FF',
            selectforeground='#FFF', relief=FLAT, bd=0)
        self.text_content.pack(side=LEFT, fill='both', expand=1)

        # The vertical scrollbar.
        self.scroll_vbar = Scrollbar(self.frame, orient=VERTICAL)
        self.scroll_vbar.pack(fill='y', side=RIGHT)

        # The vertical scrollbar needs to be linked to the text widget that has
        # the user content otherwise the scrollbar will not scroll the text.
        self.text_content.config(yscrollcommand=self.scroll_vbar.set)
        self.scroll_vbar.config(command=self.text_content.yview)

        # Style:
        self.font_family = "Helvetica"
        self.font_height = 12
        self.font_style  = "normal"

        self.font = (self.font_family, self.font_height, self.font_style)
        self.text_ln.config(font=self.font)
        self.text_content.config(font=self.font)

        self.text_content.tag_configure("bold", font=(self.font_family, self.font_height, "bold"))
        self.text_content.tag_configure("misspelled", foreground="red", underline=True)


        # Events:
        self.update_line_numbers()

        self.text_content.insert('1.0',"""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vitae nulla velit. Sed et libero ante, et hendrerit purus. Morbi volutpat porttitor eros id congue. Mauris congue, mi blandit vulputate lobortis, turpis tellus cursus felis, et venenatis arcu mi vel metus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin in risus eget urna porta sagittis. Suspendisse accumsan, nulla a lobortis tincidunt, lorem massa rhoncus erat, id rutrum magna mauris id odio. Aliquam id urna tellus. Aliquam est mi, convallis sodales gravida vitae, iaculis sed felis. Ut ultricies varius eros at egestas. Pellentesque ac enim eget arcu aliquet cursus eget sit amet nunc. Mauris eu elit enim. Phasellus volutpat ligula at quam ullamcorper ultrices et sed nisl. Quisque nisi tellus, blandit ullamcorper fringilla vel, fringilla vel ante. Aenean lectus justo, imperdiet a tempus sed, vulputate fermentum felis.

Aliquam erat volutpat. Duis justo enim, luctus eu faucibus sit amet, ultrices et tortor. Etiam feugiat justo sit amet turpis tristique tempus. Aenean non libero sed massa scelerisque tempor. Morbi suscipit, magna et aliquam tristique, ante lectus euismod purus, nec pulvinar felis purus in turpis. Aliquam erat volutpat. Maecenas in nibh tortor. Vivamus id lacus arcu, ut elementum orci. Sed fringilla, metus ac varius pretium, turpis est cursus purus, et pellentesque sapien nisi facilisis purus. Sed viverra, dolor non auctor dapibus, sem felis tristique lacus, sit amet pellentesque nulla turpis sed massa. Curabitur congue urna at ante semper non luctus felis varius. Curabitur nisl libero, lacinia vel pretium at, ornare et dolor. Quisque commodo luctus nisl non dictum.""")

        self.create_autocompleteDB(self.text_content.get('1.0', END))
        self.correct_words = open('dbs/words').read().split('\n')

        self.ac_ideal = ''
        self.text_content.bind("<Any-KeyPress>", self.handle_keypress)

        return

    def get_line_numbers(self):
        # Reset the line numbers to be empty.
        temp_str_ln = ''

        flavor = '%s\n'

        search = '@0,%d'
        line = ''
        column = ''

        curr_line = ''
        curr_column = ''

        self.max_line = 0

        # Divide the height of the text widget that contains the contents by
        # approximately the font height, i.e. for every line in the text widget.
        for div in range(0,self.text_content.winfo_height(), self.font_height):
            # Get the line and column number of the 1st character in every line
            # in the text widget. Each line in the text widget does not
            # correalate to a actual line of text because the text in a text
            # widget can be wrapped.
            line, column = self.text_content.index(search % div).split('.')

            # If the current line number in our numbering is equal to the found
            # line number:
            if curr_line == line:
                # If the current column number in our numbering is not equal to
                # the found column number, i.e. the line is wrapped:
                if curr_column != column:
                    # Set our current column number to the found column number.
                    curr_column = column
                    # Since we have found that the line is wrapped, the no new
                    # line number needs to be added, instead we append a newline
                    # character to the line numbering string.
                    temp_str_ln += '\n'
            # Else the current line number in our numbering is not equal to the
            # found line number, i.e. we have encountered a new line.
            else:
                # Set the current line and column numbers to the ones found in
                # the search.
                curr_line, curr_column = line, column
                # Add the curren line number to our main line numbering string.
                temp_str_ln += flavor % curr_line

        # Save the max line number in the current window.
        return temp_str_ln, curr_line

    def update_line_numbers(self):
        temp_str_ln, temp_max_num = self.get_line_numbers()
        if self.str_ln != temp_str_ln:
            self.str_ln = temp_str_ln
            self.text_ln.config(state='normal')

            self.text_ln.config(width=len(temp_max_num))
            self.text_ln.delete('1.0', END)
            self.text_ln.insert('1.0', self.str_ln)

            self.text_ln.config(state='disabled')

        self.text_content.after(self.update_interval, self.update_line_numbers)

        return

    def handle_spacebar(self, event):
        self.text_content.edit_separator()
        return

    def set_ideal(self, char, verbose=False):
        line, col = self.text_content.index(INSERT).split(".")
        fragment = self.text_content.get(
            '%s.%s wordstart' % (line, int(col)-1), INSERT) + char

        if verbose: print 'Fragment:', fragment
        if len(fragment) > 2 and re.match('\w+', fragment):
            if verbose: print 'Fragment:', fragment

            sug = sorted(self.suggest_autocomplete(fragment))
            if len(sug) > 0:
                if verbose: print 'Suggest:', sug[0]
                if fragment != sug[0]:
                    if verbose: print 'Insert:', sug[0][len(fragment):]
                    curr = self.text_content.index(INSERT)
                    self.ac_ideal = sug[0][len(fragment):]

                    self.text_content.insert(
                        INSERT,
                        self.ac_ideal)
                    self.text_content.mark_set(INSERT, curr)



        return

    def handle_keypress(self, event, verbose=False):
        if verbose: print 'Starting handle_keypress() w/', event.char

        # User pressed the spacebar.
        if event.char == ' ':
            # Add a separator on the undo/redo stack.
            self.text_content.edit_separator()

            # There exist a autocomplete word.
            if self.ac_ideal != '':
                # Delete the exisitng autocomplete word from the box.
                self.text_content.delete(
                    INSERT,
                    '%s+%dc' % (INSERT, len(self.ac_ideal)))

                # Delete the exisitng autocomplete word.
                self.ac_ideal = ''

            self.declare_misspell()
        # User pressed the return key.
        elif event.keysym == 'Return':
            # There exist a autocomplete word.
            if self.ac_ideal != '':
                self.text_content.mark_set(
                    INSERT,
                    '%s+%dc' % (INSERT, len(self.ac_ideal)))
                self.ac_ideal = ''

                self.text_content.delete(INSERT)

                return "break"
        elif re.match('\w', event.char):
            if self.ac_ideal == '':
                self.set_ideal(event.char, True)
            else:
                if event.char == self.ac_ideal[0]:
                    self.ac_ideal = self.ac_ideal[1:]
                else:
                    # Get the current position of the insert cursor.
                    line, col = self.text_content.index(INSERT).split('.')
                    self.text_content.delete(
                        INSERT,
                        '%s.%s' % (line, int(col) + len(self.ac_ideal)))
                    self.ac_ideal = ''

        if verbose: print 'Exiting handle_keypress()'
        return

    def declare_misspell(self):
        index = self.text_content.search(r'\s', INSERT, backwards=True, regexp=True)

        if index == "":
            index ="1.0"
        else:
            index = self.text_content.index("%s+1c" % index)

        word = self.text_content.get(index, INSERT)
        if word.encode('utf-8') in self.correct_words:
            self.text_content.tag_remove("misspelled", index, "%s+%dc" % (index, len(word)))
        else:
            self.text_content.tag_add("misspelled", index, "%s+%dc" % (index, len(word)))

        return


    def create_autocompleteDB(self, content):
#        if not os.path.exists(self.BASE_DIR+'/autocomplete.db'):
        f = open(self.BASE_DIR+'/autocomplete.db', 'w')
        f.close()

        conn = connect(self.BASE_DIR+'/autocomplete.db')
        c = conn.cursor()


        c.execute("""create table autocomplete (
            id integer primary key autoincrement,
            word text)""")

        words = re.findall('\w+', content.lower())
        for word in words:
            if len(word) > 3:
                conn.execute("""insert into autocomplete values (
                    NULL, ?)""", (word,))

        conn.commit()
        return

    def suggest_autocomplete(self, fragment):
        conn = connect(self.BASE_DIR+'/autocomplete.db')
        c = conn.cursor()

        c.execute("""select * from autocomplete where word Like ?""", (fragment+'%',))

        res = []
        for row in c:
            res.append(row[1])

        return res

if __name__ == "__main__":
    root = Tk()
    tb = TextBox(root)
    tb.frame.pack(fill='both', expand=1)
    mainloop()
