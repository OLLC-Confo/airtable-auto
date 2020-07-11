import tkinter as tk
from tkinter import messagebox, Radiobutton, IntVar, filedialog
from data import TABLE_NAME, BASE_KEY, USER_KEY, CLASS, PATH
from main import runner


master = tk.Tk()
master.title('Airtable Auto')
master.geometry("640x580")

std = tk.IntVar()
filename = ''

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

my_key = tk.Label(master, text='API key',font=('bold', 13), width=10,fg='snow',bg='grey9')
my_key.place(x=130,y=340)

my_key_val = tk.Entry(master, width=25, font=('bold',13))
my_key_val.place(x=300, y=340)

ten = tk.Radiobutton(master, text="X", variable=std, value=0)
ten.place(x=190, y=400)

eleven = tk.Radiobutton(master, text="XI", variable=std, value=1)
eleven.place(x=370,y=400)

pathname = tk.Label(master,font=('bold', 10), width=40)
pathname.place(x=100, y=442)

browsebutton = tk.Button(master, text='Select Path',width=10, command=get_path)
browsebutton.place(x=440,y=440)

submit = tk.Button(master,text="Download & Convert",bg="azure",width=50,font=("Arial",10),command=get_values)
submit.place(x=130,y=500)

master.mainloop()
