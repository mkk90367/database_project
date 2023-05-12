from tkinter import *
from tkinter import ttk
from tkinter import messagebox, Label
from tkinter_uix.Entry import Entry
import mysql.connector as sql
import modules.login as l
from modules.creds import user_pwd

def pobierz_dane(email):
    global name, location, gen, clicid
    q = f'select CName,CLocation,CGender,CID from mydb.client where CEmail="{email}"'
    mycon = sql.connect(host='localhost', user='root',
	passwd=user_pwd, database='mydb')


    cur = mycon.cursor()
    cur.execute(q)
    d = cur.fetchall()
    mycon.close()
    name = d[0][0]
    location = d[0][1]
    gen = d[0][2]
    clicid = d[0][3]
	
def logi(root):
    try:
        bg.destroy()
    except:
        pass
    l.log(root)
	
def aplikuj(table):
   
    selectedindex = table.focus()    
    selectedvalues = table.item(selectedindex, 'values')
    ajid = selectedvalues[0]
    chkquery = f'SELECT * from mydb.application where cid={clicid} and jid={ajid}'
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(chkquery)
    tempbuff = cur.fetchall()
    mycon.close()
    if(tempbuff):
        messagebox.showinfo('Uwaga', 'Wygląda na to, że już złożyłeś wniosek o tę pracę')
    else:
        queryapplyjob = f'Insert into application values(NULL,(select rid from mydb.job where job.jid={ajid}),{ajid},{clicid})'
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute(queryapplyjob)
        mycon.commit()
        mycon.close()
        messagebox.showinfo('Twój wniosek został złożony')
	
		
def usun(table):
    selectedindex = table.focus()
    selectedvalues = table.item(selectedindex, 'values')
    aaid = selectedvalues[0]
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'delete from mydb.application where aid={aaid}')
    mycon.commit()
    mycon.close()
    messagebox.showinfo('Twój wniosek został złożony')
    moje_aplikacje()
	
def sortuj_wszystkiePrace(table):
    criteria = search_d.get()
    if(criteria == "Select"): 
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute(
            f'select job.JID,job.JobRole,job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.Qualification, job.MinExp, job.Salary from mydb.job JOIN mydb.recruiter ON job.rid=recruiter.rid order by {criteria}')
        jobs = cur.fetchall()
        mycon.close()
        i = 0
        for r in jobs:
            table.insert('', i, text="", values=(
                r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
            i += 1

def sortuj_mojeAplikacje(table):
    criteria = search_d.get()
    if(criteria == "Select"):
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute(
            f'SELECT application.aid,job.JobRole, job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.qualification, job.minexp, job.salary FROM application JOIN recruiter ON application.rid=recruiter.rid JOIN job ON application.jid=job.jid where application.CID={clicid} order by {criteria}')
        jobs = cur.fetchall()
        mycon.close()
        i = 0
        for r in jobs:
            table.insert('', i, text="", values=(
                r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
            i += 1

def wyswietl_prace(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'select job.JID,job.JobRole,job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.Qualification, job.MinExp, job.Salary from mydb.job JOIN mydb.recruiter ON job.rid=recruiter.rid')
    jobs = cur.fetchall()
    mycon.close()
    i = 0
    for r in jobs:
        table.insert('', i, text="", values=(
            r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
        i += 1

def wyswietl_aplikacje(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'SELECT application.aid,job.JobRole, job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.qualification, job.minexp, job.salary FROM application JOIN recruiter ON application.rid=recruiter.rid JOIN job ON application.jid=job.jid where application.CID={clicid}')
    applications = cur.fetchall()
    mycon.close()
    print(applications)
    i = 0
    for x in applications:
        table.insert('', i, text="", values=(
            x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))
        i += 1	

def dos_prace():
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

search_l = Label(rt, text="Sortuj po : ", font=(
        'normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=(
        'normal', 18), state='readonly')
    search_d['values'] = ('Wybierz', 'Stanowisko', 'Wymiar Pracy', 'Nazwa Firmy')
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=0, pady=10)
    search = Button(rt, text="Sortuj", font=('normal', 12, 'bold'),
                    bg="#00b9ed", fg="#ffffff", command=lambda: sortuj_wszystkiePrace(table))
    search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)

    apl = Button(rt, text="Aplikuj", font=('normal', 12, 'bold'),
                 bg="#00b9ed", fg="#ffffff", command=lambda: aplikuj(table))
    apl.grid(row=0, column=4, padx=10, pady=10, ipadx=5)	
	
	scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('JID', 'JobRole', 'JobType', 'CompanyName', 'CompanyLocation', 'Qualification', 'MinExp', 'Salary'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("JID", text="ID")
    table.heading("JobRole", text="Stanowisko")
    table.heading("JobType", text="Wymiar pracy")
    table.heading("CompanyName", text='Nazwa Firmy')
    table.heading("CompanyLocation", text="Lokalizacja firmy")
    table.heading("Qualification", text='Kwalifikacje')
    table.heading("MinExp", text='Minimalne Doświadczenie')
    table.heading("Salary", text="Wynagrodzenie")
	
	table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)
	
	table.column("JID", width=100)
    table.column("JobRole", width=150)
	table.column("JobType", width=150)
    table.column("CompanyName", width=150)
    table.column("CompanyLocation", width=150)
    table.column("Qualification", width=100)
    table.column("MinExp", width=150)
    table.column("Salary", width=150)
    wyswietl_prace(table)
    table.pack(fill="both", expand=1)
    mycon.close()
	
def moje_aplikacje():
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()
	
    search_l = Label(rt, text="Sortuj po : ", font=('normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d	
	
	search_d['values'] = ('Wybierz', 'Stanowisko', 'Wymiar Pracy', 'Nazwa Firmy')
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=0, pady=10)
    search = Button(rt, text="Sortuj", font=('normal', 12, 'bold'), bg="#00b9ed",
                    fg="#ffffff", command=lambda: sortuj_mojeAplikacje(table))
    search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)

    dlt = Button(rt, text="Usuń", font=('normal', 12, 'bold'),
                 bg="#00b9ed", fg="#ffffff", command=lambda: usun(table))
    dlt.grid(row=0, column=4, padx=10, pady=10, ipadx=5)
	
	scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('AID', 'JobRole', 'JobType', 'CompanyName', 'CompanyLocation', 'Qualification', 'MinExp', 'Salary'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
	
	table.heading("AID", text="ID")
    table.heading("JobRole", text="Stanowisko")
    table.heading("JobType", text="Wymiar pracy")
    table.heading("CompanyName", text='Nazwa Firmy')
    table.heading("CompanyLocation", text="Lokalizacja firmy")
    table.heading("Qualification", text='Kwalifikacje')
    table.heading("MinExp", text='Minimalne Doświadczenie')
    table.heading("Salary", text="Wynagrodzenie")
    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("AID", width=50)
    table.column("JobRole", width=150)
    table.column("JobType", width=150)
    table.column("CompanyName", width=150)
    table.column("CompanyLocation", width=150)
    table.column("Qualification", width=100)
    table.column("MinExp", width=150)
    table.column("Salary", width=150)
    wyswietl_aplikacje(table)
    table.pack(fill="both", expand=1)
    mycon.close()
	
def client(root, email1):
    global email
    email = email1
    bg = Frame(root, width=1050, height=700)
    bg.place(x=0, y=0)

    pobierz_dane(email)

    bg.load = PhotoImage(file=f'elements\\bg{gen}.png')
    img = Label(root, image=bg.load)
    img.place(x=0, y=0)
	
	#Góra 
	
    nm = Label(root, text=f'{name}', font=(
        'normal', 36, 'bold'), bg="#ffffff", fg="#0A3D62")
    nm.place(x=300, y=50)
    cp = Label(root, text=f'{location}', font=(
        'normal', 24), bg="#ffffff", fg="#0A3D62")
    cp.place(x=300, y=120)
    bn = Button(root, text="Wyloguj się", font=('normal', 20),
                bg="#b32e2e", fg="#ffffff", command=lambda: logi(root))
    bn.place(x=800, y=75)
	
	#Lewa
	
	lf = Frame(root, width=330, height=440, bg="#ffffff")
    lf.place(x=60, y=240)
    pj = Button(lf, text="Dostępne Prace", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=dos_prace)
    pj.grid(row=0, column=0, padx=60, pady=70)
    ap = Button(lf, text="Moje aplikacje", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=moje_aplikacje)
    ap.grid(row=1, column=0, padx=60, pady=70)
	
	#Prawo
	
	
	global rt, tab, bgr
    rt = Frame(root, width=540, height=420, bg="#ffffff")
    rt.place(x=450, y=220)
    tab = Frame(root, bg="#FFFFFF")
    tab.place(x=460, y=300, width=520, height=350)
    bgrf = Frame(root, width=540, height=420)
    bgrf.load = PhotoImage(file="elements\\bgr.png")
    bgr = Label(root, image=bgrf.load, bg="#00b9ed")
    bgr.place(x=440, y=210)
	