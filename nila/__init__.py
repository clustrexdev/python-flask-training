from flask import Flask, redirect, url_for, request, render_template, make_response, session, abort, flash
from flask_mail import Mail, Message
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sample import callSample
from contactForm import ContactForm
app = Flask(__name__)
mail = Mail(app)
app.secret_key = 'nilas random string'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'snila@clustrex.com'
app.config['MAIL_PASSWORD'] = '********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
conn = sqlite3.connect('database.db')
print "Opened database successfully"

db = SQLAlchemy(app)
class students(db.Model):
  id = db.Column('student_id', db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  city = db.Column(db.String(50))  
  addr = db.Column(db.String(200))
  pin = db.Column(db.String(10))

  def __init__(self, name, city, addr, pin):
    self.name = name
    self.city = city
    self.addr = addr
    self.pin = pin
# db.create_all()

## Routing and variable rules
@app.route('/hello')
def hello():
   return render_template('hello.html')

@app.route('/hello/<user>')
def hello_name(user):
   return render_template('hello.html', name = user)

## URL Building
@app.route('/admin')
def hello_admin():
  return 'Hello Admin'

@app.route('/user/<name>')
def hello_user(name):
  return 'Hello %s' % name

@app.route('/guest/<name>')
def hello_guest(name):
  if(name == 'admin'):
    return redirect(url_for('hello_admin'))
  else:
    return redirect(url_for('hello_user',name=name))

##  HTTP Methods
@app.route('/success/<name>')
def success1(name):
  return 'Hello %s' %name

# @app.route('/login', methods = ['GET','POST'])
# def login():
#   if request.method == 'POST':
#     user = request.form['nm']
#     return redirect(url_for('success',name = user))
#   else:
#     user = request.args.get('nm')
#     return redirect(url_for('success',name = user))

@app.route('/calculateScore/<int:score>')
def calculateScore(score):
   return render_template('score.html', marks = score)

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)

## Flask - mail
@app.route("/mail")
def mail():
   msg = Message('Flask Mail Check', sender = 'nilas116@gmail.com', recipients = ['pram@clustrex.com','kavi@clustrex.com'])
   msg.body = "Hi I am sending this mail from Flask"
   mail.send(msg)
   return "Sent"

## Flask - cookies
@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
   if request.method == 'POST':
    user = request.form['nm']
   resp = make_response(render_template('readcookie.html'))
   resp.set_cookie('userID', user)
   
   return resp

@app.route('/getcookie', methods = ['POST', 'GET'])
def getcookie():
   name = request.cookies.get('userID')
   return '<h1>welcome '+name+'</h1>'


## Flask - sessions
@app.route('/sessionLogin')
def sessionLogin():
   if 'username' in session:
      username = session['username']
      return 'Logged in as ' + username + '<br>' + \
         "<b><a href = '/logout'>click here to log out</a></b>"
   return "You are not logged in <br><a href = '/loginSession'></b>" + \
      "click here to log in</b></a>"

@app.route('/loginSession', methods = ['GET', 'POST'])
def loginSession():
   if request.method == 'POST':
      session['username'] = request.form['username']
      return redirect(url_for('sessionLogin'))
   return '''
   <form action = "" method = "post">
      <p><input type = text name = username /></p>
      <p><input type = submit value = Login /></p>
   </form>
   '''

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
   # remove the username from the session if it is there
  session.pop('username', None)
  return redirect(url_for('sessionLogin'))


## Redirect & Errors
@app.route('/redirectIndex')
def redirectIndex():
   return render_template('login.html')

@app.route('/loginRedirect',methods = ['POST', 'GET'])
def loginRedirect():
   if request.method == 'POST':
      if request.form['username'] == 'admin' :
         return redirect(url_for('success'))
      else:
         abort(401)
   else:
      return redirect(url_for('redirectIndex'))

@app.route('/success')
def success():
   return 'logged in successfully'

## Flash - Message Flashing
@app.route('/loginMessage')
def loginMessage():
   return render_template('loginMessage.html')

@app.route('/loginUsingPassword', methods = ['GET', 'POST'])
def loginUsingPassword():
   error = None
   
   if request.method == 'POST':
      if request.form['username'] != 'admin' or \
         request.form['password'] != 'admin':
         error = 'Invalid username or password. Please try again!'
      else:
         flash('You were successfully logged in')
         return redirect(url_for('loginMessage'))
			
   return render_template('loginWithPassword.html', error = error)

## File Upload
@app.route('/upload')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

## upload from other
# app.add_url_rule('/', view_func = callSample)

## WTF
@app.route('/contact', methods = ['GET', 'POST'])
def contact():
   form = ContactForm()
   
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('contact.html', form = form)
      else:
         return render_template('success.html')
   elif request.method == 'GET':
         return render_template('contact.html', form = form)

## Sqlite
@app.route('/enternew')
def new_student():
   return render_template('student1.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   msg = "nothing done"
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sqlite3.connect("database.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)

## SqlAlchemy
@app.route('/')
def show_all():
   return render_template('show_all.html', students = students.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student = students(request.form['name'], request.form['city'],
            request.form['addr'], request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

if __name__ == '__main__':
   app.run(debug = True)