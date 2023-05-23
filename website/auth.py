from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
import sqlite3
import random
import os
import subprocess as sp
from speech import *
from website.otp import *
from website.email import *

con = sqlite3.connect("userinfo.db",check_same_thread=False)
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS login( namee varchar,email varchar,password varchar, phone varchar )")

cur.execute("CREATE TABLE IF NOT EXISTS community( namee varchar,message varchar)")

cur.execute("CREATE TABLE IF NOT EXISTS communitynames( id varchar,namee varchar)")

auth = Blueprint('auth', __name__)
number = 0
password = 0
email = 0
login = False
atype = 0
name = 0
diary = 0
rr = 0
age = 0
nickname = 0
status = 0
extProc = 0

@auth.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  global  login
  if login!= True :
   if request.method == "POST":
    global password
    emailornum = request.form.get('emailornum')
    password = request.form.get('password')
    print(emailornum,password)
    cur.execute("select * from login")
    my_data = cur.fetchall()
    msc = 0
    record = 0
    for i in my_data:
        print(i)
        if emailornum in i:
            msc += 1
            record = i
            break
        else:
            continue
    if msc == 0:
        flash('Invalid Email or Username', category='error')

    else:
        if password != record[2]:
            flash('Incorrect password', category='error')

        else:
                global email
                global number
                global name
                name = record[0]
                email = record[1]
                password = record[2]
                number = record[3]

                login = True
                return redirect(url_for("auth.home2"))




   return render_template("login.html", user=current_user)
  else:
      return redirect(url_for('auth.home2'))


@auth.route('/home', methods=['GET', 'POST'])
def home2():
    return render_template("mhome.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    global login
    if login!= True:
     if request.method == "POST":
        el = request.form.get('email')
        num = request.form.get('number')
        ne = request.form.get('name')
        passw = request.form.get('password')
        temp=[]
        if not str(num).isdigit() or len(num) != 10:
            flash("Invalid mobile number entered... ", category="error")

        else:
            cur.execute("select email,phone from login")
            data = cur.fetchall()
            for i in data:
                for j in i:
                    temp.append(j)

            if el in temp:
                flash("Email already exists...", category="error")

            elif num in temp:
                flash("Mobile Number already exists...", category="error")

            else :
                global rr
                global email
                email = el
                global number
                global password
                global name
                number=num
                password = passw
                name = ne
                rr = random.randint(100000, 999999)
                send_otp(rr,email)
                flash("Otp sent on Email",category="success")
                return redirect(url_for("auth.otp"))

     return render_template("signup.html", user=current_user)

    else:
      return redirect(url_for('auth.home'))

@auth.route('/otp', methods=['GET', 'POST'])
def otp():
    global email
    global number
    global name
    global password
    global rr

    if request.method =="POST" :
        eotp = request.form.get('eotp')
        print(eotp)
        print(rr)
        if not eotp.isdigit() or len(eotp)!=6:
            flash("Invalid otp", category="error")
        else:
            if int(eotp)!=rr:
                flash("Incorrect Otp",category="error")
            else :
                cur.execute("insert into login values('{}','{}','{}','{}')".format(name, email, password,number))
                con.commit()
                flash("Account Created Kindly Login",category="success")
                return  redirect(url_for("auth.login"))

    return render_template("otp.html", user=current_user)


@auth.route('/yoga', methods=['GET', 'POST'])
def yoga():
    return render_template("yoga.html", user=current_user)



@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    global email
    global atype
    global name
    global number
    global login
    global age
    global diary
    email = 0
    atype = 0
    name = 0
    number = 0
    login = False
    age = 0
    diary = 0
    return redirect(url_for("auth.home"))



@auth.route('/community', methods=['GET', 'POST'])
def community():

    cur.execute("select id from communitynames")
    d = cur.fetchall()
    c=0
    global name
    global number
    id = name + number
    for i in d:
        if id in i:
            c+=1
        else:
            continue
    if c==0:
        return redirect(url_for("auth.nicknameform"))
    else:

        cur.execute("select namee from communitynames where id ='{}'".format(id))
        n = cur.fetchall()
        cur.execute("select * from community")
        messages = cur.fetchall()
        fgh = [messages,n[0][0]]
        if request.method == "POST":
            message = request.form.get('text')
            cur.execute("insert into community values ('{}','{}')".format(n[0][0],message))
            con.commit()
            return redirect(url_for("auth.community"))
        return render_template("community.html", user=current_user,data=fgh)


@auth.route('/talk', methods=['GET', 'POST'])
def talk():
    sp.call(["python","speech.py"])
    return redirect(url_for("auth.char"))

@auth.route('/char', methods=['GET', 'POST'])
def char():
    return render_template("AI-CHAT.html", user=current_user, data=[])

@auth.route('/stopt', methods=['GET', 'POST'])
def stopt():
    p = sp.Popen(["python","speech.py"], stdout=sp.PIPE)
    p.terminate()
    return redirect(url_for("auth.char"))

@auth.route('/nicknameform', methods=['GET', 'POST'])
def nicknameform():
    if request.method == "POST":
        nam = request.form.get('name')
        global name
        global number
        id = name + number
        cur.execute("select namee from communitynames ")
        f=cur.fetchall()
        c=0
        for i in f:
            if nam in i:
                c+=1
            else :
               continue

        if c==0:
            cur.execute("insert into communitynames values ('{}','{}')".format(id,nam))
            con.commit()
            return redirect(url_for("auth.community"))

        else:
           flash("Nickname Already Taken",category="error")
           return redirect(url_for("auth.community"))
    return render_template("nickname.html", user=current_user, data=[])



@auth.route('/tracking', methods=['GET', 'POST'])
def tracking():
    import detection as d
    d.main()
    return redirect(url_for("auth.yoga"))


@auth.route('/stracking', methods=['GET', 'POST'])
def stracking():
    import  detection as ddd
    ddd.stopping()
    return redirect(url_for("auth.yoga"))

@auth.route('/suryatracking', methods=['GET', 'POST'])
def suryatracking():
    import suryanamaskaar as ssnm
    ssnm.main()
    return redirect(url_for("auth.yoga"))


@auth.route('/stopsurya', methods=['GET', 'POST'])
def stopsurya():
    import suryanamaskaar as ssnm
    ssnm.stop()
    return redirect(url_for("auth.yoga"))



@auth.route('/booking', methods=['GET', 'POST'])
def bookinf():
    global email
    mail(email)
    return redirect(url_for("auth.home2"))

