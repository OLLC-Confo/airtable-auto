from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar
import tkinter as tk
import os


def get_path():
    filename = filedialog.askdirectory()
    
master = tk.Tk()
master.title('Airtable Auto')
master.geometry("640x320")
filename = os.path.abspath(os.curdir)

page_name = tk.Label(master,text="Airtable Auto Emailer",width=32,height=1,font=("bold",25),bg="sky blue")
page_name.place(x=12,y=15)

pathname = tk.Label(master,font=('bold', 10), width=40)
pathname.config(text=os.path.abspath(os.curdir))
pathname.place(x=100, y=85)

browsebutton = tk.Button(master, text='Change Path',width=10, command = get_path)
browsebutton.place(x=440,y=85)

submit = tk.Button(master,text="Send Email",bg="azure",width=50,font=("Arial",10))        #Uncomment command and add respective function name
submit.place(x=100,y=145)

progress = Progressbar(master, orient = tk.HORIZONTAL, length = 360, mode = 'determinate')
progress.place(x = 120, y = 205)

progress_text = tk.Label(master, text="Done!",font=('bold', 13), width=5)
progress_text.place(x=500, y=205)

master.mainloop()
