from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cly12896;PWD=Q5dKJaYrZ4llJrzF",'','')
print(conn)
print("success")

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('registration and login.html')
@app.route('/view')
def view():
    return render_template('ViewJob.html')
@app.route('/apply')
def apply():
    return render_template('ApplyJob.html')
