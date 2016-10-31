from flask import Flask, render_template, request, url_for, json, send_from_directory
from flask_mail import Mail, Message


app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(port=5000, debug=True)