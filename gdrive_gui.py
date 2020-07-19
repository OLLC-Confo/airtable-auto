from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar
from gdrive import upload_all
import tkinter as tk
import os


master = tk.Tk()
master.title('Airtable Auto')
master.geometry("640x440")
std = tk.IntVar()
completed = 0
filename = os.path.abspath(os.curdir)

division_map = {
    'X': ['A','B','C','D','E','F','G'],
    'XI': ['A','B','C','D','E','F']
}


def get_values():
    global filename, master
    if lecture_val.get() != '':
        if filename != '':
            lecture = lecture_val.get()
            if std.get() == 0:
                CLASS = 'X'
            else:
                CLASS = 'XI'
            PATH = str(filename.replace('/', '\\') )
            confirm = messagebox.askyesno(
                "askyesno",
                f'''Do you wish to upload all files from to GDrive?

Selected Folder: {PATH}

Note: This will create new folders with name '{lecture}' in the respective directories of class {CLASS}.
'''
            )
            if confirm:
                try:
                    upload_all(lecture, PATH, CLASS)
                except Exception as e:
                    print(e)
                master.destroy()
        else:
            messagebox.showerror('ERROR', 'Enter the lecture name.')
    else:
        messagebox.showerror('ERROR', 'Put in the right input')

def get_path():
    global pathname, filename
    filename = filedialog.askdirectory()
    pathname.config(text=filename)


page_name = tk.Label(master,text="GDrive Uploading",width=32,height=1,font=("bold",25),bg="sky blue")
page_name.place(x=12,y=15)

lecture_label = tk.Label(master,text="Lecture Name",font=("bold",13),width=20,fg="snow",bg="grey9")
lecture_label.place(x=100,y=150)

lecture_val = tk.Entry(master,width=25,font=("bold",13))
lecture_val.place(x=300,y=150)

ten = tk.Radiobutton(master, text="X", variable=std, value=0)
ten.place(x=190, y=220)

eleven = tk.Radiobutton(master, text="XI", variable=std, value=1)
eleven.place(x=370,y=220)

pathname = tk.Label(master,font=('bold', 10), width=40)
pathname.config(text=os.path.abspath(os.curdir))
pathname.place(x=60, y=300)

browsebutton = tk.Button(master, text='Choose Submissions Folder',width=22, command=get_path)
browsebutton.place(x=360,y=300)

upload = tk.Button(master,text="Upload All",bg="azure",width=54,font=("Arial",10),command=get_values)
upload.place(x=100,y=360)

master.mainloop()
