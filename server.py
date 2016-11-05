from flask import Flask, render_template, request, url_for, json, send_from_directory
from flask_mail import Mail, Message
import mysql.connector
import smtplib
from math import *

app = Flask(__name__)

from werkzeug import SharedDataMiddleware
import os
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
  '/': os.path.join(os.path.dirname(__file__), 'static')
})


## CHECK DATABASE CONNECTION ##


conn = mysql.connector.connect(
    user='root',
    password='',
    host='127.0.0.1',
    port=3306,
    database='wt')

cur = conn.cursor()
print("DATABASE CONNECTED")


##### ROUTING TABLE  ########

@app.route("/")
def index():
    return render_template('index.htm')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/predict")
def predictloader():
    return render_template('predict2.html')

@app.route("/portal")
def portal():
    conn = mysql.connector.connect(
        user='root',
        password='',
        host='127.0.0.1',
        port=3306,
        database='wt')

    cur = conn.cursor()

    query = ("SELECT * FROM `webtech` order by `ischeckedin` asc")
    cur.execute(query)
    conn.close()

    return render_template('portal.html', cur=cur)




##### STATIC VIEWS END #######


### EMAIL STACK RELATED ###

user ="idawebtech@gmail.com"
pwd = "sanjay12"


def send_email(recipient,name,risk):
    subject = "Risk Analysis"
    body = "Hi " + name + ",\n\n" + "We have received your details and here is our analysis. \n\nRisk % = " + str(risk) + "%"
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(user, pwd)
    server.sendmail(FROM, TO, message)
    server.close()

### EMAIL STACK RELATED ENDS ###

## DYNAMIC ROUTES AND API ENDPOINTS ##


## USED TO CHECK IF APPOINTMENT ALREADY EXISTS
@app.route("/check", methods=['POST'])
def check():

    data = request.get_json()# but data will be empty unless the request has the proper content-type header...

    conn = mysql.connector.connect(
        user='root',
        password='',
        host='127.0.0.1',
        port=3306,
        database='wt')

    data = data['date'].split('/')
    newdate = data[2] + '-' + data[0] + '-' + data[1]
    print("got request:", newdate)
    cur = conn.cursor()
    # date in yyyy-mm-dd
    # query = ()
    cur.execute("SELECT COUNT(*) FROM `webtech` WHERE date = %s", (newdate, ))

    val = False

    for i in cur:
        print(i[0])
        if i[0] < 3:
            val = True

    conn.close()

    return json.dumps({'success': True, 'data': val}), 200, {'ContentType': 'application/json'}



## USED TO MAKE AN APPOINTMENT
@app.route("/doappoint", methods=['POST', 'GET'])
def appointment():

    name = request.form.get('name')
    email = request.form.get('email')
    date = request.form.get('date')

    conn = mysql.connector.connect(
        user='root',
        password='',
        host='127.0.0.1',
        port=3306,
        database='wt')

    cur = conn.cursor()

    insert_stmt = (
        "INSERT INTO webtech (DATE, NAME, EMAIL, ISCHECKEDIN) "
        "VALUES (%s, %s, %s, %s)"
    )

    data = (date, name, email, "0")

    print( cur.execute(insert_stmt, data) )

    conn.commit()
    cur.close()
    conn.close()

    return json.dumps({'success': True, 'data': 'temp'}), 200, {'ContentType': 'application/json'}



## USED TO CHECK-IN THE PATIENT
@app.route("/checkin", methods=['POST', 'GET'])
def checkin():

    email = request.form.get('email')

    conn = mysql.connector.connect(
        user='root',
        password='',
        host='127.0.0.1',
        port=3306,
        database='wt')

    cur = conn.cursor()

    insert_stmt = "UPDATE webtech SET ISCHECKEDIN= 1 WHERE EMAIL = %s"

    data = (email, )

    print(cur.execute(insert_stmt, data))

    conn.commit()
    cur.close()
    conn.close()

    return json.dumps({'success': True, 'data': 'temp'}), 200, {'ContentType': 'application/json'}

## USED TO CALCULATE PATIENT RISK
@app.route("/predictrisk", methods=['POST', 'GET'])
def predict():

    # age = 45
    # sbp = 150
    # ht = 0
    # bmi = 34
    # pri = 160
    # sm = 1
    # hf = 1

    name = request.form.get('name')
    email = request.form.get('email')
    age = int(request.form.get('age'))
    sbp =  int(request.form.get('sbp'))
    ht =  int(request.form.get('ht'))
    bmi = int(request.form.get('bmi'))
    pri =  int(request.form.get('pri'))
    sm =  int(request.form.get('sm'))
    hf =  int(request.form.get('hf'))


    ans = pow(1.3, pow((ceil((age - 44.5) / 5) + trunc((sbp - 160) / 160) + ht + ceil((bmi - 29) / 30) + (
    trunc(pri / 160) + trunc(pri / 200)) + ceil(5 - trunc((age - 45) / 10)) * sm + (
                        (fabs(10 - (trunc((age - 45) / 10) * 4)) + (10 - (trunc((age - 45) / 10)) * 4)) / 2) * hf),
                       2) / 25)
    print(ans)

    send_email(email, name, ans)

    return json.dumps({'success': True, 'data': 'temp', 'emailSent':'true'}), 200, {'ContentType': 'application/json'}



## DYNAMIC ROUTES AND API ENDPOINTS END ##

if __name__ == "__main__":
    app.run(port=5000, debug=True)