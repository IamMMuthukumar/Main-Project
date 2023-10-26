from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
# from werkzeug.utils import secure_filename


import mysql.connector
import sys, fsdk, math, ctypes, time
import datetime

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' or request.form['password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceattendancedb')
            cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)

        else:
            return render_template('index.html', error=error)


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceattendancedb')
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/Remove")
def Remove():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceattendancedb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from   regtb where Regno= '"+id +"'")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceattendancedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/AttendanceInfo")
def AttendanceInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceattendancedb')
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM attentb")
    data = cur.fetchall()
    return render_template('AttendanceInfo.html', data=data)


@app.route("/NewStudent")
def NewStudent():
    import LiveRecognition  as liv

    liv.att()
    del sys.modules["LiveRecognition"]
    return render_template('NewStudent.html')


@app.route("/NewStudent1", methods=['GET', 'POST'])
def NewStudent1():
    if request.method == 'POST':
        regno = request.form['regno']
        name = request.form['name']
        gender = request.form['gender']
        Age = request.form['Age']
        email = request.form['email']
        pnumber = request.form['pnumber']
        address = request.form['address']
        Degree = request.form['Degree']
        depart = request.form['depart']
        year1 = request.form['year1']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceattendancedb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into regtb values('" + regno + "','" + name + "','" + gender + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + Degree + "','" + depart + "','" + year1 + "')")
        conn.commit()
        conn.close()
    return render_template("AdminHome.html")


@app.route("/AUserSearch", methods=['GET', 'POST'])
def AUserSearch():
    if request.method == 'POST':

        if request.form["submit"] == "Search":
            date = request.form['date']
            date1 = request.form['date1']

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceattendancedb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM attentb where date between  '" + date + "' and  '" + date1 + "'")
            data = cur.fetchall()

            return render_template('AttendanceInfo.html', data=data)

        elif request.form["submit"] == "Close":

            date = request.form['date']
            regtb = ''
            mobile = ''

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceattendancedb')
            cursor = conn.cursor()
            cursor.execute("select *  from regtb ")
            data = cursor.fetchall()
            for i in data:
                regtb = i[0]
                print(i[0])
                Deg = i[7]
                Depar = i[8]
                Yea = i[9]
                mobile = i[5]

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceattendancedb')
                cursor = conn.cursor()
                cursor.execute("select * from attentb where Date='" + str(date) + "' and Regno='" + str(regtb) + "'")
                data = cursor.fetchone()
                if data is None:
                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='1faceattendancedb')
                    cursor = conn.cursor()
                    cursor.execute(
                        "insert into attentb values('','" + str(date) + "','" + str(
                            timeStamp) + "','" + str(Deg) + "','" + str(Depar) + "','" + str(Yea) + "','" + str(
                            regtb) + "','0')")
                    conn.commit()
                    conn.close()
                    sendmsg(mobile, "Absent For College Today")

            conn.close()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceattendancedb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM attentb where date='" + date + "'")
            data = cur.fetchall()

            return render_template('AttendanceInfo.html', data=data)


@app.route("/searchid")
def searchid():
    # eid= request.args.get('eid')
    # session['eid']=eid



    import LiveRecognition1  as liv1
    liv1.examvales()

    # liv1.att()

    # print(ExamName)

    del sys.modules["LiveRecognition1"]

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceattendancedb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM attentb where date='" + str(date) + "'")
    data1 = cur.fetchall()
    return render_template('Attendance.html', data=data1)










def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://smsserver9.creativepoint.in/api.php?username=fantasy&password=596692&to=" + targetno + "&from=FSSMSS&message=Dear user  your msg is " + message + " Sent By FSMSG FSSMSS&PEID=1501563800000030506&templateid=1507162882948811640")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
