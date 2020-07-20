from tkinter import messagebox, filedialog
from functions import LectureSubmission
from tkinter.ttk import Progressbar
import tkinter as tk
import os


master = tk.Tk()
master.title('Airtable Auto')
master.geometry("640x620")
std = tk.IntVar()
completed = 0
filename = os.path.abspath(os.curdir)

def runner(TABLE_NAME, BASE_KEY, USER_KEY, CLASS, PATH, master):
    global completed, progress, progress_text
    try:
        L = LectureSubmission(BASE_KEY, USER_KEY, TABLE_NAME, PATH, CLASS)
        L.create_empty_folders()
        print('Number of files:' , L.count)
        print('Converting data...')

        for step in L.create_pdf():
            if step == True:
                completed += 1
                progress['value'] = completed / L.count * 100
                progress_text.config(text=str(completed) + "/" + str(L.count))
                progress.update()
                progress_text.update()

    except Exception as e:
        print(e)
    
    master.destroy()

def get_values():
    global filename, master
    if table_name_val.get() != '' and base_key_val.get() != '' and  my_key_val.get() != '':
        if filename != '':
            TABLE_NAME = table_name_val.get()
            BASE_KEY = base_key_val.get()
            USER_KEY = my_key_val.get()
            if std.get() == 0:
                CLASS = 'X'
            else:
                CLASS = 'XI'
            PATH = str(filename.replace('/', '\\') )
        print(TABLE_NAME, BASE_KEY, USER_KEY, CLASS, PATH)
        runner(TABLE_NAME, BASE_KEY, USER_KEY, CLASS, PATH, master)     
    else:
        messagebox.showerror('ERROR', 'Put in the right input')        
    
def get_path():
    global pathname, filename
    filename = filedialog.askdirectory()
    pathname.config(text=filename)

page_name = tk.Label(master,text="Airtable Auto",width=32,height=1,font=("bold",25),bg="sky blue")
page_name.place(x=12,y=15)

table_name = tk.Label(master,text="Table Name",font=("bold",13),width=10,fg="snow",bg="grey9")
table_name.place(x=130,y=150)

table_name_val = tk.Entry(master,width=25,font=("bold",13))
table_name_val.place(x=300,y=150)

base_key = tk.Label(master,text="Base Key",font=("bold",13),width=10,fg="snow",bg="grey9")
base_key.place(x=129,y=240)

base_key_val = tk.Entry(master,width=25,font=("bold",13))
base_key_val.place(x=300,y=240)

my_key = tk.Label(master, text='Your key',font=('bold', 13), width=10,fg='snow',bg='grey9')
my_key.place(x=130,y=340)

my_key_val = tk.Entry(master, width=25, font=('bold',13))
my_key_val.place(x=300, y=340)

ten = tk.Radiobutton(master, text="X", variable=std, value=0)
ten.place(x=190, y=400)

eleven = tk.Radiobutton(master, text="XI", variable=std, value=1)
eleven.place(x=370,y=400)

pathname = tk.Label(master,font=('bold', 10), width=40)
pathname.config(text=os.path.abspath(os.curdir))
pathname.place(x=100, y=442)

browsebutton = tk.Button(master, text='Change Path',width=10, command=get_path)
browsebutton.place(x=440,y=440)

submit = tk.Button(master,text="Download & Convert",bg="azure",width=50,font=("Arial",10),command=get_values)
submit.place(x=100,y=500)

progress = Progressbar(master, orient = tk.HORIZONTAL, length = 360, mode = 'determinate')
progress.place(x = 120, y = 560)

progress_text = tk.Label(master, text="Ready",font=('bold', 13), width=5)
progress_text.place(x=500, y=560)

master.mainloop()
