import tkinter
'''
def create_empty_window():
    window = tkinter.Tk()
    message = tkinter.Label(text = "ICS32 Example GUI")
    button = tkinter.Button(master = window, text = "Press me", command=run_method)
    message.pack()
    button.pack()
    window.mainloop()



def run_method():
    print("This method was executed after you clicked on the button!")
create_empty_window()


def create_window():
    window = tkinter.Tk()
    window.geometry('300x200')
    frame = tkinter.Frame(window, height = 200, width = 300)
    frame.bind("<Enter>", _on_enter)
    frame.bind("<Leave>", _on_exit)
    frame.pack()
    window.mainloop()

def _on_enter(event):
    print(f"Mouse entered window at position {event.x}, y = {event.y}")
def _on_exit(event):
    print(f"Mouse left the window at position x = {event.x}, y = {event.y}")
create_window()
'''

def start_editor():
    root_window = tkinter.Tk()
    root_window.title("ICS32 Text Editor")
    root_window.rowconfigure(1, minsize=600)
    root_window.columnconfigure(0, minsize=600)

    edition_region = tkinter.Text(master = root_window)
    control_buttons = tkinter.Frame(master=root_window, relief=tkinter.GROOVE)
    ctr_file_open = tkinter.Button(control_buttons, text = "Open File")
    ctr_file_save = tkinter.Button(control_buttons, text= "Save file as...")
    ctr_file_open.grid(row=0, column=0, stickey = "ew", padx = 5, pady = 5)
    ctr_file_save.grid(row=0, column=1, sticky = "ew", padx=5)