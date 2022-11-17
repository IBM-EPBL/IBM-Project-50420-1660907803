import re
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
from flask_mail import Mail, Message
# print(conn)
# print("success")

app = Flask(__name__)

app.secret_key = 'a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cly12896;PWD=Q5dKJaYrZ4llJrzF", '', '')


@app.route('/')
def home():
    return render_template('registration and login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global userid
    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username=? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid = account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in succesfully'

            return render_template('ViewJob.html', msg=msg)
        else:
            msg = 'Incorrect username/password!'
    return render_template('registration and login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account Already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only alpha characters or numbers!'
        else:
            insert_sql = "INSERT INTO users VALUES(?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'you have successfully registered'
            app.config['SECRET_KEY'] = 'top-secret!'
            app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
            app.config['MAIL_PORT'] = 587
            app.config['MAIL_USE_TLS'] = True
            app.config['MAIL_USERNAME'] = 'apikey'
            app.config['MAIL_PASSWORD'] = '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'
            app.config['MAIL_DEFAULT_SENDER'] = 'jasperkirubakaranjit2019@citchennai.net'
            mail = Mail(app)
            recipient = request.form['email']
            msg = Message('Successfully Registered', recipients=[recipient])
            msg.body = ('Congratulations! You have successfully registered with '
                        'Skill/Job Recommender!')
            msg.html = ('<h1>Successfully Registered</h1>'
                        '<p>Congratulations! You have successfully registered with '
                        '<b>Skill/Job Recommender</b>!</p>')
            mail.send(msg)
            return render_template('registration and login.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('registration and login.html', msg=msg)


@app.route('/view')
def view():
    return render_template('ViewJob.html')


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        qualification = request.form['qualification']
        skills = request.form['skills']
        jobs = request.form['jobs']

        insert_sql = "INSERT INTO jobs values(?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, username)
        ibm_db.bind_param(prep_stmt, 2, email)
        ibm_db.bind_param(prep_stmt, 3, qualification)
        ibm_db.bind_param(prep_stmt, 4, skills)
        ibm_db.bind_param(prep_stmt, 5, jobs)
        ibm_db.execute(prep_stmt)
        msg = "You have succesfully applied for the job!"
        session['loggedin'] = True
        app.config['SECRET_KEY'] = 'top-secret!'
        app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USERNAME'] = 'apikey'
        app.config['MAIL_PASSWORD'] = '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'
        app.config['MAIL_DEFAULT_SENDER'] = 'jasperkirubakaranjit2019@citchennai.net'
        mail = Mail(app)
        recipient = request.form['email']
        msg = Message('Successfully Applied',
                      recipients=[recipient])
        msg.body = ('Congratulations! You have successfully applied your job with '
                    'Skill/Job Recommender!')
        msg.html = ('<h1>Successfully Applied</h1>'
                    '<p>Congratulations! You have successfully applied your job with '
                    '<b>Skill/Job Recommender</b>!</p>')
        mail.send(msg)
        return redirect(url_for('login'))

    elif request.method == 'POST':
        msg = 'Please fill the form!'
    return render_template('ApplyJob.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('registration and login.html')
