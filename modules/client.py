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