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
    global s
    stop_btn.configure(state=NORMAL)
    pause_btn.configure(state=NORMAL)
    start_btn.configure(state=DISABLED)
    s.start()
    
def pause():
    global s
    stop_btn.configure(state=NORMAL)
    pause_btn.configure(state=NORMAL)
    start_btn.configure(state=DISABLED)
    s.start()
    
def resume():
    global s
    pause_btn.configure(text="Pause", command=pause)
    s.resume()
    
def pause():
    global s
    pause_btn.configure(text="Resume", command=resume)
    s.pause()
    
def stop():
    global s
    stop_btn.configure(state=DISABLED)
    pause_btn.configure(state=DISABLED)
    start_btn.configure(state=NORMAL)
    s.stop()

# Buttons.
start_btn = ttk.Button(btn_frame, text="Start", command=start, state=NORMAL)
start_btn.grid(row=0,column=0, sticky=E,padx=3,pady=3)

pause_btn = ttk.Button(btn_frame, text="Pause", command=pause, state=DISABLED)
pause_btn.grid(row=0,column=1, sticky=NS,padx=3,pady=3)

stop_btn = ttk.Button(btn_frame, text="Stop", command=stop, state=DISABLED)
stop_btn.grid(row=0,column=2,sticky=W,padx=3,pady=3)

root.mainloop()