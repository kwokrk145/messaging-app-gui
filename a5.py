'''Module for running messaging app'''
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Text
import Profile
import ds_messenger
import time
import pathlib
from server_commands import connect_server


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event=None):
        '''Show chosen user'''
        try:
            index = int(self.posts_tree.selection()[0])
            entry = self._contacts[index]
            if self._select_callback is not None:
                self.delete_entries()
                self._select_callback(entry)
        except IndexError:
            pass

    def insert_contact(self, contact: str):
        '''Insert contact into tree'''
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        '''Insert contact into tree'''
        if len(contact) > 25:
            contact = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def delete_tree(self):
        '''Delete text in tree'''
        items = self.posts_tree.get_children()
        for i in items:
            self.posts_tree.delete(i)

    def insert_user_message(self, message: str):
        '''Insert user message to the right'''
        font = ("Times New Roman", 11)
        self.entry_editor.tag_configure("custom_font", font=font)
        self.entry_editor.insert(tk.END, message + '\n',
                                 ('entry-right', 'custom_font'))

    def insert_contact_message(self, message: str, notice=None):
        '''Insert user message to the left'''
        font = ("Times New Roman", 11)
        if notice:
            font = ("Times New Roman", 11, "bold")
        self.entry_editor.tag_configure("custom_font", font=font)
        self.entry_editor.insert(tk.END, message + '\n',
                                 ('entry-left', 'custom_font'))

    def delete_entries(self):
        '''Delete entries'''
        self.entry_editor.delete(1.0, tk.END)

    def get_text_entry(self) -> str:
        '''Return text entry in box'''
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self):
        '''Set text entry'''
        self.message_editor.delete(1.0, tk.END)

    def correct_login(self, user, pw):
        '''Error for wrong login'''
        if not user or not pw:
            message = "Wrong username or password\n"
            message += "Values must match DSU Profile Loaded"
            messagebox.showerror("Error", message)

    def not_connected(self):
        '''Error for not connected'''
        message = "You must open a profile and connect "
        message += "to the server before sending a message!"
        messagebox.showerror("Error", message)

    def connection_error(self):
        '''Error for connection error'''
        message = "Something went wrong when connecting "
        message += "to DSU Server\nPlease try again."
        messagebox.showerror("Error", message)

    def unopened(self):
        '''Error for unopened'''
        message = "Please open a profile first."
        messagebox.showerror("Error", message)

    def _draw(self):
        '''Draw visuals'''
        posts_frame = tk.Frame(master=self, width=250, bg="#73d2de")
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="#C0DFFF")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="#C0DFFF")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="#C0DFFF", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="#C0DFFF")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0,
                                      height=5, bg="#C0DFFF")
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0,
                                    height=5, bg="#C1D1C9")
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    '''Class for footer visual and functions'''

    def __init__(self, root, send_callback=None, send_callback2=None):
        '''Define important attributes'''
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._send_callback2 = send_callback2
        self._draw()

    def send_click(self):
        '''Send button command'''
        if self._send_callback is not None:
            self._send_callback()

    def add(self):
        '''add contact button'''
        if self._send_callback2 is not None:
            self._send_callback2()

    def _draw(self):
        '''Draw visual'''
        save_button = tk.Button(master=self, text="Send", width=20)
        save_button.configure(command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        add_button = tk.Button(master=self, text="Add Contact", width=20)
        add_button.configure(command=self.add)
        add_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=10, pady=10)


class NewContactDialog(tk.simpledialog.Dialog):
    '''Visual and return information'''

    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        '''Define attribute'''
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        self.bio = None
        super().__init__(root, title)

    def body(self, frame):
        '''Draws visual'''
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        if self.server:
            self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        if self.user:
            self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = '*'
        if self.pwd:
            self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        '''Gather information'''
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class NewFile(tk.simpledialog.Dialog):
    '''Draw visuals and gather information'''

    def __init__(self, root, title=None, user=None, pwd=None, bio=None):
        '''Define important attributes'''
        self.root = root
        self.user = user
        self.pwd = pwd
        self.bio = None
        super().__init__(root, title)

    def body(self, frame):
        '''Draws visuals'''
        self.usr_label = tk.Label(frame, width=30, text="Username")
        self.usr_label.pack()
        self.usr_entry = tk.Entry(frame, width=30)
        if self.user:
            self.usr_entry.insert(tk.END, self.user)
        self.usr_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = '*'
        if self.pwd:
            self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

        self.bio_label = tk.Label(frame, width=30, text="Bio")
        self.bio_label.pack()
        self.bio_entry = tk.Entry(frame, width=30)

        if self.bio:
            self.bio_entry.insert(tk.END, self.bio)
        self.bio_entry.pack()

    def apply(self):
        '''Gather information'''
        self.user = self.usr_entry.get()
        self.pwd = self.password_entry.get()
        self.bio = self.bio_entry.get()


class MainApp(tk.Frame):
    '''Main frame'''

    def __init__(self, root):
        '''Define attributes'''
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.profile = None
        self.path = None
        self.bio = None
        self.check = False
        self.direct_messenger = None
        self.start = True
        self._draw()

    def _switch(self):
        '''Switch user'''
        topic = f"Chat history with {self.recipient}"
        line = "-" * 113
        self.body.insert_contact_message(topic)
        self.body.insert_contact_message(line)
        info = self.profile.get_messages(self.recipient)
        for m in info:
            message = m[1]
            if len(message) >= 35:
                message = message[0:35] + "\n" + message[35:]
            if m[0] == "myself":
                if "You" not in message:
                    message = "You: " + message
                self.body.insert_user_message(message)
            elif m[0] == self.recipient:
                if self.recipient not in message:
                    message = self.recipient + ": " + message
                self.body.insert_contact_message(message)

    def reset(self):
        '''Resets information'''
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.profile = None
        self.path = None

    def send_message(self):
        '''Send message'''
        if self.profile and not self.recipient:
            message = "Please select a person to chat with."
            messagebox.showerror("Notice", message)
        else:
            message = self.body.get_text_entry()
            self.body.node_select()
            user = self.recipient
            if self.recipient and self.username and self.server:
                self.direct_messenger.send(message, user)
                message = "You: " + message
                self.publish(message, "myself")
                self.body.set_text_entry()
                self.profile.add_message(message, time.time(), user, "myself")
                self.profile.save_profile(self.path)
            else:
                self.body.not_connected()

    def add_contact(self):
        '''Add contact'''
        if self.profile:
            m = "Enter name of new contact"
            name = tk.simpledialog.askstring("Add Contact", m)
            if name:
                self.body.insert_contact(name)
                self.profile.add_friend(name)
                self.profile.save_profile(self.path)
        else:
            self.body.unopened()

    def recipient_selected(self, recipient):
        '''Recipient select'''
        self.recipient = recipient
        self._switch()

    def configure_server(self):
        '''Configure server information'''
        if self.profile:
            previous = self.profile.dsuserver
            ud = NewContactDialog(self.root, "Configure Account",
                                  self.username, self.password, self.server)
            self.username = ud.user
            self.password = ud.pwd
            self.server = ud.server
            self.profile.dsuserver = self.server
            try:
                if self.username is None and self.password is None \
                                and self.server is None:
                    pass
                elif self.username != self.profile.username or \
                    self.password != self.profile.password and \
                        self.server is not None:
                    self.body.correct_login(False, False)
                else:
                    if self.server is None:
                        pass
                    elif connect_server("", self.server, 3021, "yes"):
                        t = ds_messenger.DirectMessenger(self.server,
                                                         self.username,
                                                         self.password)
                        mage = "Connected to server!"
                        messagebox.showinfo("Notice", mage)
                        self.direct_messenger = t
                        self.check = True
                        self.profile.save_profile(self.path)
                    else:
                        self.body.connection_error()
                        self.profile.dsuserver = previous
                        self.profile.save_profile(self.path)
                        self.server = None
            except AttributeError:
                pass
        else:
            if self.start:
                message = "Please open a profile first!"
                messagebox.showerror("Notice", message)
            else:
                self.body.unopened()

    def publish(self, message: str, kind):
        '''Puts on screen'''
        if kind == "myself":
            self.body.insert_user_message(message)
        else:
            self.body.insert_contact_message(message)

    def check_new(self):
        '''Check for new messages'''
        if self.recipient and self.check:
            obj = self.direct_messenger.retrieve_new()
            if obj:
                for item in obj:
                    sender = item.recipient
                    if sender not in self.profile.get_friends():
                        self.body.insert_contact(sender)
                        self.profile.add_friend(sender)
                    msg = item.message
                    ts = float(item.timestamp)
                    if self.recipient == sender:
                        msg = self.recipient + ": " + msg
                        self.body.insert_contact_message(msg)
                    self.profile.add_message(msg, ts, sender, sender)
                    self.profile.save_profile(self.path)

    def close(self):
        '''Close button'''
        if self.profile:
            self.body.delete_entries()
            friends = self.profile.get_friends()
            message = self.body.get_text_entry()
            self.body.set_text_entry()
            self.body.delete_tree()
            self.username = None
            self.password = None
            self.server = None
            self.recipient = None
            self.profile = None
            self.path = None
            self.instructions()
        else:
            message = "You haven't opened anything..."
            messagebox.showerror("Notice", message)

    def new_file(self):
        '''New file button'''
        file_path = filedialog.asksaveasfilename(defaultextension=".dsu")
        if file_path:
            ud = NewFile(self.root, "New User Information",
                         self.username, self.password, self.bio)
            self.username = ud.user
            self.password = ud.pwd
            self.bio = ud.bio
            self.server = None
            profile = Profile.Profile()
            profile.username = self.username
            profile.password = self.password
            profile.bio = self.bio
            p = pathlib.Path(file_path)
            with p.open("w", encoding='utf-8') as file:
                pass
            profile.save_profile(file_path)
            self.body.delete_entries()
            self.body.delete_tree()
            self.body.set_text_entry()
            self.profile = profile
            self.path = p
            self.instructions()
        u = self.username
        pdw = self.password
        boi = self.bio
        if file_path and (not u or not pdw or not boi):
            f_path = pathlib.Path(file_path)
            f_path.unlink()
            error = "You must fill out all the boxes! No profile created."
            messagebox.showerror("Missing Information", error)
            self.close()

    def _open_profile(self):
        '''Open profiles'''
        try:
            if self.profile:
                self.close()
            filepath = tk.filedialog.askopenfilename()
            self.path = filepath
            self.profile = Profile.Profile()
            self.profile.load_profile(filepath)
            friends = self.profile.get_friends()
            for i in friends:
                self.body.insert_contact(i)
            self.body.delete_entries()
            self.instructions()
        except Profile.DsuFileError:
            self.profile = None
            pass

    def instructions(self):
        '''Starting instructions'''
        self.body.delete_entries()
        message = " " * 40 + "Welcome to the DSU Messenging App!"
        message1 = "-" * 113
        message2 = "1. Please open a DSU profile to "
        message2 += "load contacts and old messages."
        message2 += " If not, please create a new \nprofile.\n"
        message4 = "2. Then, please connect to the DSU server. "
        message4 += "If you forgot your username or password,"
        message4 += " please hit view information under the Messenger Info."
        message5 = "\n3. To add contact, "
        message5 += "please hit add contact button at the bottom."
        message5 += " Hit close in settings to close your\ncurrent profile."
        self.body.insert_contact_message(message, "bold")
        self.body.insert_contact_message(message1)
        self.body.insert_contact_message(message2)
        self.body.insert_contact_message(message4)
        self.body.insert_contact_message(message5)
        final = "\nNOTE to ADMIN: Please start with new file first "
        final += "since DSU Profile format changed"
        self.body.insert_contact_message(final)

    def view_information(self):
        '''View profile information'''
        self.body.delete_entries()
        if self.profile:
            intro = " " * 59 + "User Information\n" + "-" * 113
            show = self.profile.dsuserver
            if not show:
                show = "None (Suggested: 168.235.86.101)"
            message1 = f"DSU Address: {show}"
            message2 = f"Username: {self.profile.username}"
            message3 = f"Password: {self.profile.password}"
            self.body.insert_contact_message(intro)
            self.body.insert_contact_message(message1)
            self.body.insert_contact_message(message2)
            self.body.insert_contact_message(message3)
        else:
            error = "Notice: You haven't opened a profile "
            error += "and or connected to the server yet."
            self.body.insert_contact_message(error)

    def _draw(self):
        '''Draw visual'''
        f = ("Times New Roman", 10, "bold")
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', font=f, command=self.new_file)
        menu_file.add_command(label='Open...', font=f,
                              command=self._open_profile)
        menu_file.add_command(label='Close', font=f, command=self.close)

        settings_file = tk.Menu(menu_bar)
        instructions = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        menu_bar.add_cascade(menu=instructions, label="Messenger Info")
        settings_file.add_command(label='Configure DS Server', font=f,
                                  command=self.configure_server)
        instructions.add_command(label="How to use", font=f,
                                 command=self.instructions)
        instructions.add_command(label='View Information', font=f,
                                 command=self.view_information)
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message,
                             send_callback2=self.add_contact)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
        la = tk.Label(self.root, text="Contacts", bg="white",
                      font=("Times New Roman", 11, "bold"))
        la.place(x=78, y=6)
        add_button = tk.Button(master=self, text="Add Contact", width=20)
        add_button.configure(command=self.add_contact)
        add_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)
        if not self.path:
            self.instructions()


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("800x700")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    def update():
        app.check_new()
        main.after(2000, update)
    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.after(2000, update)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
