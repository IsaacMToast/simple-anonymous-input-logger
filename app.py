from tkinter import *
from tkinter import ttk
from session import Session

# Initialize root.
root = Tk()
root.title("Simple Input Logger.")
root.geometry("250x75")

# Button container.
btn_frame = ttk.Frame(root)
btn_frame.pack()

started = False
s = Session("testa")

def start():
    global started, s
    started = True
    stop_btn.configure(state=NORMAL)
    start_btn.configure(state=DISABLED)
    s.start()
    
def stop():
    global started, s
    started = False
    stop_btn.configure(state=DISABLED)
    start_btn.configure(state=NORMAL)
    s.stop()

# Start/Stop buttons.
start_btn = ttk.Button(btn_frame, text="Start", command=start, state=NORMAL)
start_btn.grid(row=0,column=0, sticky=E,padx=3,pady=3)

stop_btn = ttk.Button(btn_frame, text="Stop", command=stop, state=DISABLED)
stop_btn.grid(row=0,column=1,sticky=W,padx=3,pady=3)\

root.mainloop()