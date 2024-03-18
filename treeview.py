import tkinter as tk
from tkinter import ttk

class Body(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = []
        self._draw()

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            contact = contact[:24] + "..."
        self.posts_tree.insert('', id, id, text=contact)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        # Add a couple of contacts for demonstration
        self.insert_contact("John Doe")
        self.insert_contact("Alice Smith")
        self.insert_contact("boo")
        self.insert_contact("boo")
        self.insert_contact("boo")
        self.insert_contact("boo")
        self.insert_contact("boo")
        self.insert_contact("boo")
        self.insert_contact("boo")
        self.insert_contact("boo")
        self.insert_contact("boo")
        self.insert_contact("boo")

# Create a root window
root = tk.Tk()
root.geometry("300x200")
root.title("Contact List")

# Create a Body instance and pack it into the root window
body = Body(root)
body.pack(fill=tk.BOTH, expand=True)

# Start the Tkinter event loop
root.mainloop()
