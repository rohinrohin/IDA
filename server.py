from flask import Flask, render_template, request, url_for, json, send_from_directory
import mysql.connector
import smtplib
import psycopg2
from math import *
import sendgrid
import os
from sendgrid.helpers.mail import *

app = Flask(__name__)

from werkzeug import SharedDataMiddleware
import os
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
  '/': os.path.join(os.path.dirname(__file__), 'static')
})


## CHECK DATABASE CONNECTION ##


conn = psycopg2.connect(
    user='admin',
    password='admin',
    host='127.0.0.1',
    port=5432,
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
    return render_template('predict.html')

@app.route("/portal")
def portal():
    conn = psycopg2.connect(
        user='admin',
        password='admin',
        host='127.0.0.1',
        port=5432,
        database='wt')

    cur = conn.cursor()

    query = ("SELECT * FROM webtech order by ischeckedin asc")
    cur.execute(query)
    
    ren = render_template('portal.html', cur=cur)
    conn.close()
    return ren

@app.route("/gallery")
def gallery():
    return render_template('gallery.html')

@app.route("/awareness")
def awareness():
    return render_template('awareness.html')


##### STATIC VIEWS END #######


### EMAIL STACK RELATED ###

user ="idawebtech@gmail.com"
pwd = "sanjay12"

def send_email_sg(recipient, name, risk):
    sg = sendgrid.SendGridAPIClient(apikey='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')
    from_email = Email("idawebtech@gmail.com")
    to_email = Email("rohinrohin@gmail.com ")
    subject = "Thank you for trying IDA!"
    content = Content("text/html", "<h4 style=\"color:#4A235A;font-family: verdana;\">Hi " + name + ",\n\n" + "</h4><h4 style=\"font-family: verdana;\">Thanks for your interest in our prediction engine,<br> \n\n We have received your details and here is our analysis. <br>Risk Level = " + str(ceil(risk)) + "%<br> You can further visit http://127.0.0.1:5000/awareness for more information on reducing your risk percentage.</h4><h4 style=\"color:#4A235A;font-family: verdana;\">Regrads, <br>IDA, Webtech Team</h4>")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def send_email(recipient,name,risk):
    subject = "Risk Analysis"
    body = "<h4 style=\"color:#4A235A;font-family: verdana;\">Hi " + name + ",\n\n" + "</h4><h4 style=\"font-family: verdana;\">Thanks for your interest in our prediction engine,<br> \n\n We have received your details and here is our analysis. <br>Risk Level = " + str(ceil(risk)) + "%<br> You can further visit http://127.0.0.1:5000/awareness for more information on reducing your risk percentage.</h4><h4 style=\"color:#4A235A;font-family: verdana;\">Regrads, <br>IDA, Webtech Team</h4>"
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nMIME-Version: 1.0\nContent-type: text/html\nSubject: %s\n\n%s
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
    
    data = request.form.get('date')  # but data will be empty unless the request has the proper content-type header...
    conn = psycopg2.connect(
        user='admin',
        password='admin',
        host='127.0.0.1',
        port=5432,
        database='wt')

    print("got request:", data)
    cur = conn.cursor()
    # date in yyyy-mm-dd
    # query = ()
    cur.execute("SELECT COUNT(*) FROM webtech WHERE date = %s", (data, ))

    val = False

    for i in cur:
        print(i[0])
        if i[0] < 3:
            val = True

    conn.close()

    return str(val)



## USED TO MAKE AN APPOINTMENT
@app.route("/doappoint", methods=['POST', 'GET'])
def appointment():

    name = request.form.get('name')
    email = request.form.get('email')
    date = request.form.get('date')

    conn = psycopg2.connect(
        user='admin',
        password='admin',
        host='127.0.0.1',
        port=5432,
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

    return "true"



## USED TO CHECK-IN THE PATIENT
@app.route("/checkin", methods=['POST', 'GET'])
def checkin():

    email = request.form.get('email')

    conn = psycopg2.connect(
        user='admin',
        password='admin',
        host='127.0.0.1',
        port=5432,
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
    print("inside risk")

    name = request.form.get('name')
    email = request.form.get('email')
    age = int(request.form.get('age'))
    sbp = int(request.form.get('sbp'))
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

    send_email_sg(email, name, ans)

    return "true"



## DYNAMIC ROUTES AND API ENDPOINTS END ##

if __name__ == "__main__":
    app.run(port=5000, debug=True)