from tkinter import *
from tkinter import messagebox
from tkinter_uix.Entry import Entry
import mysql.connector as sql
from modules.register import *
from modules.recruiter import *
from modules.client import *
from modules.creds import user_pwd

def sukces(root, email1):
    global f
    f1.destroy()
    try:
        r1.destroy()
    except:
        pass

    s = f'select type from users where email="{email1}"'
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(s)
    q = cur.fetchall()
    mycon.close()
    print(q)

    if q[0][0] == "recruiter":
        rec(root, email1)
    else:
        cli(root, email1)

def sprawdzanie(root):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute('select email,password from users')
    total = cur.fetchall()
    mycon.close()
    email1 = email.get()
    password = pwd.get()
    if email1 and password:
        for i in total:
            if email1 == i[0] and password == i[1]:
                return sukces(root, email1)
            elif email1 == i[0] and password != i[1]:
                messagebox.showinfo('Uwaga!', 'Nieprawidlowe dane rejestracyjne')
                break
        else:
            messagebox.showinfo(
                'Uwaga!', 'Email nie jest zarejestrowany, Prosze sie zarejestrowac')
    else:
        messagebox.showinfo(
            'Uwaga!', 'Prosze wprowadzic adres email oraz haslo')

def reg(root):
    try:
        f1.destroy()
    except:
        pass
    mai(root)

def log(root):
    global f1, email, pwd
    try:
        f2.destroy()
    except:
        pass
    f1 = Frame(root, width=1050, height=700, bg='#FFFFFF')
    f1.place(x=0, y=0)

    # Tlo
    f1.render = PhotoImage(file='elements\\bg.png')
    img = Label(f1, image=f1.render)
    img.place(x=0, y=0)

    # Email
    email_l = Label(f1, text="Email : ", bg='#FFFFFF',
                    font=('normal', 20, 'bold'), fg="#00B9ED")
    email_l.place(x=600, y=300)
    email = Entry(f1, width=24, placeholder="Wprowadz email..")
    email.place(x=720, y=300)

    # Haslo
    pwd_l = Label(f1, text="Haslo : ", bg='#FFFFFF',
                  font=('normal', 20, 'bold'), fg="#00B9ED")
    pwd_l.place(x=600, y=350)
    pwd = Entry(f1, show="*", width=24, placeholder="Wprowadz haslo..")
    pwd.place(x=720, y=350)

    # Przyciski
    f1.bn = PhotoImage(file="elements\\login2.png")
    btn = Button(f1, image=f1.bn, bg='#FFFFFF', bd=0,
                 activebackground="#ffffff", command=lambda: sprawdzanie(root))
    btn.place(x=820, y=420)

    f1.bn1 = PhotoImage(file="elements\\reg.png")
    btn1 = Button(f1, image=f1.bn1, bg='#FFFFFF', bd=0,
                  activebackground="#ffffff", command=lambda: reg(root))
    btn1.place(x=620, y=420)
