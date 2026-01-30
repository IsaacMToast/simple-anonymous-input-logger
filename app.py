from tkinter import *
from tkinter import ttk
from session import Session

# Initialize root.
root = Tk()
root.title("Simple Input Logger.")
root.geometry("250x32")
root.resizable(False, False)

# Create new session.
session = Session("unnamed")

def start():
    global session
    stop_btn.configure(state=NORMAL)
    pause_btn.configure(state=NORMAL)
    start_btn.configure(state=DISABLED)
    session.start()
    
def resume():
    global session
    pause_btn.configure(text="Pause", command=pause)
    session.resume()
    
def pause():
    global session
    pause_btn.configure(text="Resume", command=resume)
    session.pause()
    
def stop():
    global session
    stop_btn.configure(state=DISABLED)
    pause_btn.configure(state=DISABLED)
    start_btn.configure(state=NORMAL)
    resume()
    session.stop()

# Button frame.
btn_frame = ttk.Frame(root)
btn_frame.pack(fill="both", expand=True)

# Buttons.
start_btn = ttk.Button(btn_frame, text="Start", command=start, state=NORMAL)
start_btn.grid(row=0, column=0, sticky=E)

pause_btn = ttk.Button(btn_frame, text="Pause", command=pause, state=DISABLED)
pause_btn.grid(row=0, column=1, sticky=NS)

stop_btn = ttk.Button(btn_frame, text="Stop", command=stop, state=DISABLED)
stop_btn.grid(row=0, column=2, sticky=W)

# Distribute weights.
for c in range(3):
    btn_frame.columnconfigure(c, weight=1)

root.mainloop()