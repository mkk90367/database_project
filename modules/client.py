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
    myapp()

