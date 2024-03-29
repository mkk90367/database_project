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
    nm = Label(root, text=f'{name}', font=('normal', 36, 'bold'), bg="#ffffff", fg="#0A3D62")
    nm.place(x=300, y=50)
    cp = Label(root, text=f'{company}', font=('normal', 24), bg="#ffffff", fg="#0A3D62")
    cp.place(x=300, y=120)
    bn = Button(root, text="Wyloguj się", font=('normal', 20), bg="#b32e2e", fg="#ffffff", command=lambda: logi(root))
    bn.place(x=800, y=75)

    # lewa czesc
    lf = Frame(root, width=330, height=440, bg="#ffffff")
    lf.place(x=60, y=220)

    cj = Button(lf, text="Opublikuj ofertę\npracy", font=('normal', 16), bg="#b32e2e", fg="#ffffff", command=utworz)
    cj.grid(row=0, column=0, padx=80, pady=40)

    pj = Button(lf, text="Zamieszczone\noferty pracy", font=('normal', 16), bg="#b32e2e", fg="#ffffff", command=zamieszczone)
    pj.grid(row=1, column=0, padx=80, pady=40)

    ap = Button(lf, text="Wszystkie\naplikacje", font=('normal', 16), bg="#b32e2e", fg="#ffffff", command=aplikowania)
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
    role_l = Label(tab, text="Stanowisko:", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    role_l.grid(row=0, column=0, pady=10, padx=10)
    type_l = Label(tab, text="Wymiar pracy :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    type_l.grid(row=1, column=0, pady=10, padx=10)
    qual_l = Label(tab, text="Kwalifikacje :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    qual_l.grid(row=2, column=0, pady=10, padx=10)
    exp_l = Label(tab, text="Doświadczenie :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    exp_l.grid(row=3, column=0, pady=10, padx=10)
    sal_l = Label(tab, text="Wynagrodzenie :", font=(
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
    jtype['values'] = ('Umowa o pracę', 'Umowa zlecenie','B2B', 'Staż' )
    jtype.current(0)
    jtype.grid(row=1, column=1, pady=10, padx=10)
    qual = Entry(tab, placeholder="Wprowadz kwalifikacje zaw.")
    qual.grid(row=2, column=1, pady=10, padx=10)
    exp = Entry(tab, placeholder="Wprowadz minimalne dosw.")
    exp.grid(row=3, column=1, pady=10, padx=10)
    sal = Entry(tab, placeholder="Wprowadz oczekiwane zarobki")
    sal.grid(row=4, column=1, pady=10, padx=10)
    
    btn = Button(tab, text="Wyślij", font=(20), bg="#45CE30",
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
            messagebox.showinfo('UWAGA!', 'Prosze wprowadzić typ pracy')
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
                messagebox.showinfo('SUKCES!', 'Pomyślnie utworzono oferte pracy')
            except:
                pass
    else:
        messagebox.showinfo('UWAGA!', 'Uwaga wypełnij wyszystkie obowiązkowe pola')

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
    if kryteria == "Stanowisko":
        kryteria = "JobRole"
    elif kryteria == "Wymiar Pracy":
        kryteria = "JobType"
    elif kryteria == "Kwalifikacje":
        kryteria = "Qualification"
    elif kryteria == "Doświadczenie":
        kryteria = "MinExp"
    elif kryteria == "Wynagrodzenie":
        kryteria = "Salary"
    
    if kryteria == "Wybierz":
        table.delete(*table.get_children())
    else:
        mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute(f'select RID,JID, JobRole, JobType, Qualification, MinExp, Salary FROM mydb.Job where RID={recid} order by {kryteria}')
        all_jobs = cur.fetchall()
        mycon.close()

        table.delete(*table.get_children())
        i = 0
        for r in all_jobs:
            table.insert('', i, text="", values=(r[1], r[2], r[3], r[4], r[5], r[6]))
            i += 1

# -------------------------------------------------Usuwanie zamieszczonej oferty pracy-------------------------


def usuwaniePracy(table):
    wybranyIndex = table.focus()
    wybranaWartosc = table.item(wybranyIndex, 'values')
    ajid = wybranaWartosc[0]
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(f'delete from mydb.application where jid={ajid}')
    cur.execute(f'delete from mydb.job where jid={ajid}')
    mycon.commit()
    mycon.close()
    messagebox.showinfo('Dziekuje', 'Twoja oferta pracy zostala usunieta')
    zamieszczone()

# ----------------------------------------------Oferty zamieszczone przez rekrutera----------------------------


def zamieszczone():
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()
    
    search_l = Label(rt, text="Sortuj po: ", font=(
        'normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=(
        'normal', 18), state='readonly')
    search_d['values'] = ('Wybierz', 'Stanowisko', 'Wymiar Pracy',"Kwalifikacje","Doświadczenie" ,"Wynagrodzenie")
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=0, pady=10)
    search = Button(rt, text="Sortuj", font=('normal', 12, 'bold'),
                    bg="#00b9ed", fg="#ffffff", command=lambda: sortujWszystko(table))
    search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)
    dlt = Button(rt, text="Usuń", font=('normal', 12, 'bold'),
                 bg="#00b9ed", fg="#ffffff", command=lambda: usuwaniePracy(table))
    dlt.grid(row=0, column=4, padx=10, pady=10, ipadx=5)
    
    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")
    
    table = ttk.Treeview(tab, columns=('JID', 'JobRole', 'JobType', 'Qualification', 'MinExp', 'Salary'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("JID", text="ID_oferty_pracy")
    table.heading("JobRole", text="Stanowisko")
    table.heading("JobType", text='Wymiar Pracy')
    table.heading("Qualification", text='Kwalifikacje')
    table.heading("MinExp", text='Doświadczenie')
    table.heading("Salary", text="Wynagrodzenie")
    
    table['show'] = 'headings'
    
    scx.config(command=table.xview)
    scy.config(command=table.yview)
    
    table.column("JID", width=100)
    table.column("JobRole", width=150)
    table.column("JobType", width=150)
    table.column("Qualification", width=100)
    table.column("MinExp", width=100)
    table.column("Salary", width=150)
    pokazWszystko(table)
    table.pack(fill="both", expand=1)
    
    
# -----------------------------------------Aplikowania na oferty zamieszczone przez rekrutera------------------
def aplikowania():
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Sortuj po: ", font=('normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=(
        'normal', 18), state='readonly')
    search_d['values'] = ('Zaznacz', 'Zakres_obowiaz.', 'Nazwa_aplikanta','Email','Wiek','Lokalizacja','Płec', 'Doświadczenie','Umiejetnosci','Kwalifikacje')
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=10, pady=10)
    search = Button(rt, text="Sortuj", font=('normal', 12, 'bold'),
                    bg="#00b9ed", fg="#ffffff", command=lambda: sortujAplikantow(table))
    search.grid(row=0, column=3, padx=45, pady=10, ipadx=30)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")
    
    table = ttk.Treeview(tab, columns=('JobRole', 'CName', 'CEmail', 'CAge', 'CLocation', 'CGender', 'CExp', 'CSkills', 'CQualification'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    
    table.heading("JobRole", text="Zakres_obowiaz.")
    table.heading("CName", text='Nazwa_aplikanta')
    table.heading("CEmail", text='Email')
    table.heading("CAge", text='Wiek')
    table.heading("CLocation", text='Lokalizacja')
    table.heading("CGender", text='Płec')
    table.heading("CExp", text='Doświadczenie')
    table.heading("CSkills", text='Umiejetnosci')
    table.heading("CQualification", text='Kwalifikacje')

    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JobRole", width=150)
    table.column("CName", width=200)
    table.column("CEmail", width=100)
    table.column("CAge", width=50)
    table.column("CLocation", width=150)
    table.column("CGender", width=100)
    table.column("CExp", width=100)
    table.column("CSkills", width=200)
    table.column("CQualification", width=150)
    pokazAplikantow(table)
    table.pack(fill="both", expand=1)
    
# ----------------------------------------------Aplikanci------------------------------------------------------


def pokazAplikantow(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'SELECT job.JobRole, client.CName, client.CEmail, client.CAge, client.CLocation, client.CGender, client.CExp, client.CSkills, client.CQualification FROM application JOIN client ON application.cid=client.CID JOIN job ON job.jid=application.jid where job.rid={recid}')
    aplikanci = cur.fetchall()
    mycon.close()
    print(aplikanci)
    i = 0
    for x in aplikanci:
        table.insert('', i, text="", values=(
            x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]))
        i += 1
        
        
def sortujAplikantow(table):
    kryteria = search_d.get()
    if kryteria == "Zakres_obowiaz.":
        kryteria = "JobRole"
    elif kryteria == "Nazwa_aplikanta":
        kryteria = "CName"
    elif kryteria == "Email":
        kryteria = "CEmail"
    elif kryteria == "Wiek":
        kryteria = "CAge"
    elif kryteria == "Lokalizacja":
        kryteria = "CLocation"
    elif kryteria == "Płec":
        kryteria = "CGender"
    elif kryteria == "Doświadczenie":
        kryteria = "CExp"
    elif kryteria == "Umiejetnosci":
        kryteria = "CSkills"
    elif kryteria == "Kwalifikacje":
        kryteria = "CQualification"
    
    if kryteria == "Zaznacz":
        pass
    else:
        pass

        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')

        cur = mycon.cursor()
        cur.execute(
            f'SELECT job.JobRole, client.CName, client.CEmail, client.CAge, client.CLocation, client.CGender, client.CExp, client.CSkills, client.CQualification FROM application JOIN client ON application.cid=client.CID JOIN job ON job.jid=application.jid where job.rid={recid} order by {kryteria}')
        aplikanci = cur.fetchall()
        mycon.close()
        print(aplikanci)
        i = 0
        for x in aplikanci:
            table.insert('', i, text="", values=(
                x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]))
            i += 1