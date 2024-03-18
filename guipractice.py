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
'''

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