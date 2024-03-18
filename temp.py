import tkinter as tk
from tkinter import simpledialog

class MyDialog(tk.simpledialog.Dialog):
    def body(self, frame):
        self.name_label = tk.Label(frame, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(frame)
        self.name_entry.pack()

        self.age_label = tk.Label(frame, text="Age:")
        self.age_label.pack()
        self.age_entry = tk.Entry(frame)
        self.age_entry.pack()

    def apply(self):
        self.result = (self.name_entry.get(), self.age_entry.get())

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    dialog = MyDialog(root, "Enter Name and Age")
    #result = dialog.result

    # if result:
    #     name, age = result
    #     print("Name:", name)
    #     print("Age:", age)
    # else:
    #     print("Dialog was cancelled.")

if __name__ == "__main__":
    main()
