from tkinter import *
from tkinter import ttk
from tkinter import messagebox, Label
from tkinter_uix.Entry import Entry
import mysql.connector as sql
import modules.login as l
from modules.creds import user_pwd

def uzyskajInformacje(email):
    global name, company, gen, recid
    q = f'select RName,CompanyName,RGender,RID from mydb.recruiter where REmail="{email}"'
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(q)
    d = cur.fetchall()
    mycon.close()

    name = d[0][0]
    company = d[0][1]
    gen = d[0][2]
    recid = d[0][3]

def logi(root):
    try:
        bg.destroy()
    except:
        pass
    l.log(root)

# -------------------------------------------------------------------------------------------------------------
def rekruter(root, email1):
    global email
    email = email1
    bg = Frame(root, width=1050, height=700)
    bg.place(x=0, y=0)

    uzyskajInformacje(email)

    bg.load = PhotoImage(file=f'elements\\bg{gen}.png')
    img = Label(root, image=bg.load)
    img.place(x=0, y=0)

    # pasek nawigacyjny
    nm = Label(root, text=f'{name}', font=(
        'normal', 36, 'bold'), bg="#ffffff", fg="#0A3D62")
    nm.place(x=300, y=50)
    cp = Label(root, text=f'{company}', font=(
        'normal', 24), bg="#ffffff", fg="#0A3D62")
    cp.place(x=300, y=120)
    bn = Button(root, text="WYLOGOWANIE", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=lambda: logi(root))
    bn.place(x=800, y=75)

    # lewa czesc
    lf = Frame(root, width=330, height=440, bg="#ffffff")
    lf.place(x=60, y=220)
    cj = Button(lf, text="Umiesc oferte pracy", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=utworz)
    cj.grid(row=0, column=0, padx=80, pady=40)
    pj = Button(lf, text="Zamieszczone oferty", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=posted)
    pj.grid(row=1, column=0, padx=80, pady=40)
    ap = Button(lf, text="Aplikowania", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=app)
    ap.grid(row=2, column=0, padx=80, pady=40)

    # prawa czesc
    global rt, tab, bgr
    rt = Frame(root, width=540, height=420, bg="#ffffff")
    rt.place(x=450, y=220)
    tab = Frame(root, bg="#FFFFFF")
    tab.place(x=460, y=300, width=520, height=350)
    bgrf = Frame(root, width=540, height=420)
    bgrf.load = PhotoImage(file="elements\\bgr.png")
    bgr = Label(root, image=bgrf.load, bg="#00b9ed")
    bgr.place(x=440, y=210)

# ---------------------------------------------Umiesc ogloszenie o prace---------------------------------------
def utworz():
    global role, jtype, qual, exp, sal
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    # Tworzenie formy
    f1 = Frame(rt, width=520)
    f1.load = PhotoImage(file="elements\\create.png")
    img = Label(rt, image=f1.load, bg="#FFFFFF")
    img.grid(row=0, column=1, padx=150, pady=10)

    # Etykiety
    role_l = Label(tab, text="Rola :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    role_l.grid(row=0, column=0, pady=10, padx=10)
    type_l = Label(tab, text="Typ :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    type_l.grid(row=1, column=0, pady=10, padx=10)
    qual_l = Label(tab, text="Kwalifikacje :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    qual_l.grid(row=2, column=0, pady=10, padx=10)
    exp_l = Label(tab, text="Doswiadczenie :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    exp_l.grid(row=3, column=0, pady=10, padx=10)
    sal_l = Label(tab, text="Placa :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    sal_l.grid(row=4, column=0, pady=10, padx=10)

    # Wpisy wprowadzane za pomocą Entry
    style = ttk.Style(tab)
    style.configure("TCombobox", background="white",
                    foreground="#696969")

    role = Entry(tab, placeholder="Wprowadz stanowisko")
    role.grid(row=0, column=1, pady=10, padx=10)
    jtype = ttk.Combobox(tab, font=("normal", 18),
                         width=23, state='readonly')
    jtype['values'] = ('Select', 'FullTime', 'PartTime', 'Intern')
    jtype.current(0)
    jtype.grid(row=1, column=1, pady=10, padx=10)
    qual = Entry(tab, placeholder="Wprowadz kwalifikacje zaw.")
    qual.grid(row=2, column=1, pady=10, padx=10)
    exp = Entry(tab, placeholder="Wprowadz minimalne dosw.")
    exp.grid(row=3, column=1, pady=10, padx=10)
    sal = Entry(tab, placeholder="Wprowadz oczekiwane zarobki")
    sal.grid(row=4, column=1, pady=10, padx=10)
    
    btn = Button(tab, text="Przekaz", font=(20), bg="#45CE30",
                 fg="#FFFFFF", command=przekazOfertePracy)
    btn.grid(row=5, column=1, pady=15)
    
def przekazOfertePracy():
    global role1, jtype1, qual1, exp1, sal1
    role1 = role.get()
    jtype1 = jtype.get()
    qual1 = qual.get()
    exp1 = exp.get()
    sal1 = sal.get()
    print(role1, jtype1, qual1, exp1, sal1)
    if role1 and jtype1 and qual1 and exp1 and sal1:
        if jtype1 == "Select":
            messagebox.showinfo('UWAGA!', 'Prosze wprowadzic typ pracy')
        else:
            exe1 = f'INSERT INTO mydb.Job(RID, JID, JobRole, JobType, Qualification, MinExp, Salary) VALUES({recid}, NULL, "{role1}", "{jtype1}", "{qual1}", {exp1}, {sal1})'
            try:
                mycon = sql.connect(host='localhost', user='root',
                                    passwd=user_pwd, database='mydb')
                cur = mycon.cursor()
                cur.execute(exe1)
                role.delete(0, END)
                jtype.delete(0, END)
                qual.delete(0, END)
                exp.delete(0, END)
                sal.delete(0, END)
                mycon.commit()
                mycon.close()
                messagebox.showinfo('SUKCES!', 'Pomyslnie utworzono oferte pracy')
            except:
                pass
    else:
        messagebox.showinfo('UWAGA!', 'WSZYSTKIE POLA MUSZA BYC WYPELNIONE')

# ----------------------------------------------Zapytanie dotyczace opublikowanych ofert pracy-----------------


def pokazWszystko(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'select RID,JID, JobRole, JobType, Qualification, MinExp, Salary FROM mydb.Job where RID={recid}')
    all_jobs = cur.fetchall()
    mycon.close()
    i = 0
    for r in all_jobs:
        table.insert('', i, text="", values=(
            r[1], r[2], r[3], r[4], r[5], r[6]))
        i += 1

# --------------------------------------------Sortowanie zapytan-----------------------------------------------


def sortujWszystko(table):
    kryteria = search_d.get()
    if(kryteria == "Select"):
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')

        cur = mycon.cursor()
        cur.execute(
            f'select RID,JID, JobRole, JobType, Qualification, MinExp, Salary FROM mydb.Job where RID={recid} order by {kryteria}')
        all_jobs = cur.fetchall()
        mycon.close()
    i = 0
    for r in all_jobs:
        table.insert('', i, text="", values=(
            r[1], r[2], r[3], r[4], r[5], r[6]))
        i += 1