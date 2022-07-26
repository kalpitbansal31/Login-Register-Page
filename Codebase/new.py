from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2
import psycopg2.extras
import re
import pika
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# hostname = "192.168.112.72"
hostname = "192.168.29.4"
database = "postgres"
user_name = "postgres"
pwd = "mysecretpassword"
port_id = 9002
conn = None

conn = psycopg2.connect(host=hostname, dbname=database, user=user_name, password=pwd, port=port_id)


class RabbitMQ(object):
    def __init__(self, queue='hello'):
        self.credentials = pika.PlainCredentials('test', 'test1234')
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.62',port=5672,credentials=self.credentials))
        self._channel = self._connection.channel()
        self.queue = queue
        self._channel.queue_declare(queue=self.queue)

    def publish(self, payload={}):
        self._channel.basic_publish(exchange='',
                                    routing_key='hello',
                                    body=str(payload))
        print("Published...")



@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template(username=session['username'])
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)

        cursor.execute('SELECT * FROM userdetails WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            password_rs = account['password']
            print(password_rs)
            if check_password_hash(password_rs, password):
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return True

    return False


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cursor = conn.cursor()
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            fullname = request.form['fullname']
            username = request.form['username']
            pwd = request.form['password']
            email = request.form['email']
            server = RabbitMQ(queue='hello')
            server.publish(payload={
                "username": username,
                "fullname": fullname,
                "password": pwd,
                "email": email
            })
            print(fullname, username, email, pwd)
            _hashed_password = generate_password_hash(pwd)
            # cursor.execute("SELECT * from userdetails WHERE username= %s", (username,))
            # query = f"SELECT * FROM userdetails WHERE username = {username}"
            query = "SELECT * from userdetails WHERE username= " + f"'{username}'"
            print(query)
            cursor.execute(query)

            account = cursor.fetchone()
            print(account)

            if account:
                flash('Account already exists!')
            elif not re.match(r'[^@]+@[^@]+\.[^@+]', email):
                flash('Invalid email address!')
            elif not re.match(r'[A-Za-z0-9]+', username):
                flash('Username must contain only characters and numbers!')
            elif not username or not pwd or not email:
                flash('Please fill out the form!')
            else:
                cursor.execute("INSERT INTO userdetails(fullname, username, password, email) VALUES (%s,%s,%s,%s)",
                               (fullname, username, _hashed_password, email))
                conn.commit()

        return "Registered"
    elif request.method == 'GET':
        return 'Use POST'
    else:
        return 'Use POST'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)