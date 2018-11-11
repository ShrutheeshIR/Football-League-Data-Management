from predictions import predAttendance
from flask import Flask,redirect,url_for,request,render_template
app = Flask(__name__)
import mysql.connector
import json
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# @app.route('/hello/<hello>')
# def helloPage(hello):
#     return 'hahaha'+str(hello)

# @app.route('/h1/')
# def h1():
#     return redirect(url_for('helloPage',hello='kkk'))

# if __name__ == '__main__':
#    app.run()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="battlefield4",
  database="footballmanagement"
)
print(mydb)
session=dict()
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username']=request.form['username']
            session['password']=request.form['password']
            return redirect(url_for('home'))
    return render_template('index.html', error=error)

@app.route('/home')
def home():
    return "username is"+str(session['username'])+"password is"+str(session['password'])


@app.route('/slc')
def line():
    graphJSON=predAttendance.predatt()
    return render_template('chart.html',  graphJSON=graphJSON)

# @app.route('/')
# def start():
#     return render_template('index.html')

# @app.route('/fan')
# def fan():
#     tid = request.args.get('tid')
#     user = request.args.get('user')
#     print('welcome'+ tid)
#     return 'welcome %s !!!! teamid %s' % user % tid

# @app.route('/login',methods = ['POST', 'GET'])
# def login():
#    if request.method == 'POST':
#       user = request.form['username']
#       mycursor = mydb.cursor()
#       mycursor.execute("SELECT tid FROM user where '"+user+"'=usn;")
#       myresult = mycursor.fetchall()
#       print(myresult[0][0])
#       return redirect(url_for('fan',tid=str(myresult[0][0]),user=user))
#    else:
#       user = request.args.get('username')
#       mycursor = mydb.cursor()
#       mycursor.execute("SELECT tid FROM user where '"+user+"'=usn;")
#       myresult = mycursor.fetchall()
#       print(myresult[0][0])
#       return redirect(url_for('fan',tid=str(myresult[0][0]),user=user))

if __name__ == '__main__':
   app.run(debug = True)