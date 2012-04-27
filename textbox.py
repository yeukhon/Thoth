from Tkinter import *
import tkFont
import os
from sqlite3 import connect
import re, string


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
            selectforeground='#FFF', relief=FLAT, bd=0, wrap=WORD)
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
        self.font_slant  = "italic"
        self.font_misspell = tkFont.Font(
            family=self.font_family, size=self.font_height,
            slant=self.font_slant)

        self.font = (self.font_family, self.font_height, self.font_style)
        self.text_ln.config(font=self.font)
        self.text_content.config(font=self.font)

        self.text_content.tag_configure("bold", font=(self.font_family, self.font_height, "bold"))
        self.text_content.tag_configure("misspelled", font=self.font_misspell, foreground="red", underline=1)
        self.text_content.tag_configure("autocomplete", background="#0000ff")


        # Events:
        self.update_line_numbers()

#        self.text_content.insert('1.0',"""Thoth was considered one of the more important deities of the Egyptian pantheon. In art, he was often depicted as a man with the head of an ibis or a baboon, animals sacred to him. As in the main picture, Thoth is almost always shown holding a Was (a wand or rod symbolizing power) in one hand and an Ankh (the key of the Nile symbolizing life) in the other hand. His feminine counterpart was Seshat.
#Thoth's chief temple was located in the city of Khmun, later renamed Hermopolis Magna during the Greco-Roman era (in reference to him through the Greeks' interpretation that he was the same as their god Hermes) and Eshmunen in the Coptic rendering. In that city, he led the Ogdoad pantheon of eight principal deities. He also had numerous shrines within the cities of Abydos, Hesert, Urit, Per-Ab, Rekhui, Ta-ur, Sep, Hat, Pselket, Talmsis, Antcha-Mutet, Bah, Amen-heri-ab, and Ta-kens.
#Thoth played many vital and prominent roles in Egyptian mythology, such as maintaining the universe, and being one of the two deities (the other being Ma'at, who was also his wife) who stood on either side of Ra's boat. In the later history of ancient Egypt, Thoth became heavily associated with the arbitration of godly disputes, the arts of magic, the system of writing, the development of science, and the judgment of the dead.""")

#        self.create_autocompleteDB(self.text_content.get('1.0', END))
#        self.declare_misspell()
        self.correct_words = open('dbs/words').read().split('\n')

        self.ac_ideal = ''
        self.text_content.bind("<Any-KeyPress>", self.handle_keypress)

        self.top = master.winfo_toplevel()

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
        # approximately the font height, i.e. for every line in the text
        # widget.
        for div in range(0,self.text_content.winfo_height(), self.font_height):
            # Get the line and column number of the 1st character in every
            # line in the text widget. Each line in the text widget does not
            # correalate to a actual line of text because the text in a text
            # widget can be wrapped.
            line, column = self.text_content.index(search % div).split('.')

            # If the current line number in our numbering is equal to the
            # found line number:
            if curr_line == line:
                # If the current column number in our numbering is not equal
                # to the found column number, i.e. the line is wrapped:
                if curr_column != column:
                    # Set our current column number to the found column
                    # number.
                    curr_column = column
                    # Since we have found that the line is wrapped, the no new
                    # line number needs to be added, instead we append a
                    # newline character to the line numbering string.
                    temp_str_ln += '\n'
            # Else the current line number in our numbering is not equal to
            # the found line number, i.e. we have encountered a new line.
            else:
                # Set the current line and column numbers to the ones found in
                # the search.
                curr_line, curr_column = line, column
                # Add the curren line number to our main line numbering
                # string.
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

        self.text_content.after(
            self.update_interval, self.update_line_numbers)

        return

    def init_menus(self):
        # Create the menubar that will hold all the menus and thier items.
        self.menubar = Menu(self.frame)

        # File Pulldown menu, contains "Open", "Save", and "Exit" options.
        self.filemenu = Menu(self.menubar, tearoff=0)
        if self.document.is_memeber(self.user.info['id']):
            self.filemenu.add_command(label="Save", command=self.handler_save_file)
            self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.file_exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.top["menu"] = self.menubar
        return

    def handle_spacebar(self, event):
        self.text_content.edit_separator()
        return

    def initialize(self, user, document):
        self.user = user
        self.document = document

        self.set_content_from_doc(self.document)

        if not self.document.is_memeber(self.user.info['id']):
            self.text_content.config(state=DISABLED)

        self.init_menus()
        return

    def set_content_from_doc(self, doc):
        fhandle = open(doc.info['ppath']+str(doc.info['id']), 'r')
        contents = fhandle.read()
        fhandle.close()

        self.text_content.insert('1.0', contents)

        self.create_autocompleteDB(self.text_content.get('1.0', END))
        self.declare_misspell()

        return

    def handler_save_file(self):
        fhandle = open(self.document.info['ppath']+str(self.document.info['id']), 'w')
        contents = self.text_content.get('1.0', END)
        fhandle.write(contents)
        fhandle.close()
        return

    def file_exit(self):
        """Clean-up before exiting a file."""

        self.frame.quit()
        return

    def get_content(self):
        return self.text_content.get('1.0', END)

    def set_ideal(self, char, verbose=False):
        # User deleted a character, so there does not exist a new character;
        # however, the box will not immediately show the change.
        if char == '':
            # Get the fragment of the word the user already typed. There is a
            # delay between when the key is pressed and the box is updated.
            fragment = self.text_content.get(
                'insert-1c wordstart', 'insert-1c')
        # User typed a ASCII character.
        else:
            # Get the fragment of the word the user already typed. Assumes
            # that the insertion cursor is at the end of the word, so
            # wordstart needs the cursor to be in the word, hence the '-1c'.
            # There is a delay between when the key is pressed and the box is
            # updated.
            fragment = self.text_content.get(
                'insert-1c wordstart', INSERT) + char

        # Fragment must be at least 3 characters in length for a suggestion to
        # be given. Fragment must not contain any punctuation.
        if len(fragment) > 2 and re.match('\w+', fragment):
            if verbose: print 'Fragment:', fragment

            # Get the suggested word, sorted, so the shortest word
            # will be at the beginning of the list.
            sug = self.suggest_autocomplete(fragment)

            # There is a suggestion.
            if sug != '':
                if verbose: print 'Suggestion:', sug
                # Fragment must not be the same as suggestion for a new
                # suggestion to be made.
                if fragment != sug:
                    if verbose: print 'Insertion Fragment:', sug[len(fragment):]

                    # Save the index of the insertion cursor.
                    curr = self.text_content.index(INSERT)
                    # Set the autocomplete word to the portion that still
                    # needs to be typed.
                    self.ac_ideal = sug[len(fragment):]

                    # Insert the portion that still needs to be typed into the
                    # box.
                    self.text_content.insert(
                        INSERT, self.ac_ideal)

                    self.text_content.tag_add(
                        "autocomplete",
                        '%s-%dc' % (INSERT, len(self.ac_ideal)),
                        INSERT)

                    # Set the position of the insertion cursor to the saved
                    # position.
                    self.text_content.mark_set(INSERT, curr)

        return

    def handle_keypress(self, event, verbose=False):
        # User pressed the spacebar.
        if event.char == ' ' or event.keysym == 'Tab':
            # Add a separator on the undo/redo stack.
            self.text_content.edit_separator()

            # There exist a autocomplete word.
            if self.ac_ideal != '':
                self.text_content.tag_remove(
                    "autocomplete",
                    INSERT, '%s+%dc' % (INSERT, len(self.ac_ideal)))

                # Delete the exisitng autocomplete word from the box.
                self.text_content.delete(
                    INSERT, '%s+%dc' % (INSERT, len(self.ac_ideal)))

                # Delete the exisitng autocomplete word.
                self.ac_ideal = ''

            # Check whether the last word is misspelled.
            self.handle_misspell(verbose=True)

        # User pressed the return key.
        elif event.keysym == 'Return':
            # There exist a autocomplete word.
            if self.ac_ideal != '':
                self.text_content.tag_remove(
                    "autocomplete",
                    INSERT, '%s+%dc' % (INSERT, len(self.ac_ideal)))

                # Move the insertion cursor to after the word.
                self.text_content.mark_set(
                    INSERT, '%s+%dc' % (INSERT, len(self.ac_ideal)))
                # Reset the ideal autocomplete word.
                self.ac_ideal = ''

                # Nulls the newline character from the 'Return' keystroke.
                return "break"

        # User pressed the backspace key.
        elif event.keysym == 'BackSpace':
            # There exist a autocomplete word.
            if self.ac_ideal != '':
                self.text_content.tag_remove(
                    "autocomplete",
                    INSERT, '%s+%dc' % (INSERT, len(self.ac_ideal)))

                # Delete the autocomplete word from the box.
                self.text_content.delete(
                    INSERT, '%s+%dc' % (INSERT, len(self.ac_ideal)))
                # Reset the autocomplete word.
                self.ac_ideal = ''
                # Look for a new autocomplete word.
                self.set_ideal('', verbose=False)

        # User pressed a character key.
        elif re.match('\w', event.char):
            # There does not exist an autocomplete word.
            if self.ac_ideal == '':
                # Look for a new autocomplete word.
                self.set_ideal(event.char, verbose=False)
            # There exist an autocomplete word.
            else:
                # User typed in the next character of autocomplete word.
                if event.char == self.ac_ideal[0]:
                    # Delete the 1st character from the autocomplete word.
                    self.ac_ideal = self.ac_ideal[1:]

                    # Delete the redundant character from the box.
                    self.text_content.delete(INSERT)

                    if self.ac_ideal == '':
                         # Look for a new autocomplete word.
                        self.set_ideal(event.char, verbose=False)

                # User is not typing the autocomplete word.
                else:
                    self.text_content.tag_remove(
                        "autocomplete",
                        INSERT, '%s+%dc' % (INSERT, len(self.ac_ideal)))

                    # Delete the autocomplete word from the box.
                    self.text_content.delete(
                        INSERT, '%s+%dc' % (INSERT, len(self.ac_ideal)))
                    # Reset the autocomplete word.
                    self.ac_ideal = ''
                    # Look for a new autocomplete word.
                    self.set_ideal(event.char, verbose=False)
        else:
            # There exist a autocomplete word.
            if self.ac_ideal != '':
                self.text_content.tag_remove(
                    "autocomplete",
                    INSERT, '%s+%dc' % (INSERT, len(self.ac_ideal)))

                # Reset the autocomplete word.
                self.ac_ideal = ''

        return

    def handle_misspell(self, verbose=False):
        # There is no punctuation at the end of the word.
        if re.match('\w', self.text_content.get('insert-1c')):
            # Get the beginning index of the currently typed word.
            index = self.text_content.index('insert-1c wordstart')
        # There is punctuation at the end of the word.
        else:
            # Get the beginning index of the currently typed word.
            index = self.text_content.index('insert-2c wordstart')

        # Get the word from the starting index to the insertion cursor. Remove
        # punctuation from the word. Force the word to lowercase.
        word = re.sub('[%s]' % re.escape(string.punctuation), '',
            self.text_content.get(index, INSERT).encode('utf-8')).lower()
        if verbose: print 'Index:', index, '\tWord:', word

        # The word is valid.
        if word in self.correct_words:
            # Remove the underline tags.
            self.text_content.tag_remove(
                "misspelled", index, "%s+%dc" % (index, len(word)))

            self.add_autocompleteDB(word)

        # The word is not valid.
        else:
            # Add the underline tags.
            self.text_content.tag_add(
                "misspelled", index, "%s+%dc" % (index, len(word)))

        return

    def declare_misspell(self, verbose=False):
        # Get the contents of the box. Split the contents into words. Create
        # a set out of the list of words to remove redundant words. Create a
        # list out of the set for indexing purposes. Sort the list of words.
        words = sorted(list(set(re.findall(
            '\w+', self.text_content.get('1.0', END)))))
        if verbose: print 'Number of unique words:', len(words)

        for word in words:
            # Words in the dictionary are unicode, so convert the query word
            # to unicode. Force the word to lowercase.
            word = word.encode('utf-8').lower()
            if verbose: print 'Query Word:', word

            # The query word is not in the dictionary of valid words.
            if word not in self.correct_words:
                # Start searching for the query word in the box at '1.0'
                start = '1.0'
                # Find the first index of the query word in the box. The query
                # word must begin and end with a non-word character. Search is
                # done from the starting index to the ending index of the box.
                index = self.text_content.search(
                    '[^\w]%s[^\w]' % (word), start, stopindex=END,
                    regexp=True, nocase=1)+'+1c'

                # While the query word can be found in the box.
                while index != '+1c':
                    if verbose: print 'Misspelled Word Index:', index

                    # Add the underline tag.
                    self.text_content.tag_add(
                        "misspelled", index, "%s+%dc" % (index, len(word)))

                    # New starting index is the end of the current word.
                    start = '%s+%dc' % (index, len(word))
                    # Find the next index of the query word in the box. The
                    # query word must begin and end with a non-word character.
                    # Search is done from the starting index to the ending
                    # index of the box.
                    index = self.text_content.search(
                        '[^\w]%s[^\w]' % (word), start, stopindex=END,
                        regexp=True, nocase=1)+'+1c'

        return


    def create_autocompleteDB(self, content):
        # Create a new autocomplete database.
        f = open(self.BASE_DIR+'/autocomplete.db', 'w')
        f.close()

        # Create a connection to the autocomplete database.
        conn = connect(self.BASE_DIR+'/autocomplete.db')
        # Create a cursor to the autocomplete database.
        c = conn.cursor()

        # Create the autocomplete table.
        c.execute("""create table autocomplete (
            id integer primary key autoincrement,
            word text)""")

        # Find all the words in the provided content.
        words = re.findall('\w+', content.lower())

        for word in words:
            # Only words with a length greater than 3 character will be used
            # as suggestions.
            if len(word) > 3:
                # Insert the word into the autocomplete table.
                conn.execute("""insert into autocomplete values (
                    NULL, ?)""", (word,))

        # Commit the changes to the autocomplete database.
        conn.commit()
        # Close the connection to the autocomplete database.
        conn.close()
        return

    def add_autocompleteDB(self, word):
        # Create a connection to the autocomplete database.
        conn = connect(self.BASE_DIR+'/autocomplete.db')
        # Create a cursor to the autocomplete database.
        c = conn.cursor()

        # Search for the word.
        c.execute("""select * from autocomplete where
            word=?""",
            (word,))

        # Get 1 result.
        res = c.fetchone()

        # The result does not exist.
        if not res:
            c.execute("""insert into autocomplete values(
                NULL, ?)""", (word,))

            # Commit the changes to the autocomplete database.
            conn.commit()

        # Close the connection to the autocomplete database.
        conn.close()
        return

    def suggest_autocomplete(self, fragment):
         # Create a connection to the autocomplete database.
        conn = connect(self.BASE_DIR+'/autocomplete.db')
        # Create a cursor to the autocomplete database.
        c = conn.cursor()

        # Search for the query fragment and get only 1 result order ascending.
        c.execute("""select word from autocomplete where
            word Like ? and word != ?
            order by word asc
            limit 1""",
            (fragment+'%', fragment))

        # Get 1 result.
        res = c.fetchone()

        # Close the connection to the autocomplete database.
        conn.close()

        # The result exist.
        if res:
            return res[0]
        # The result does not exist.
        else:
            return ''

if __name__ == "__main__":
    root = Tk()
    tb = TextBox(root)
    tb.frame.pack(fill='both', expand=1)
    mainloop()
