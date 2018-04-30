from flask import Flask, redirect, url_for, request, render_template, make_response, session, abort, flash
from flask_mail import Mail, Message
from werkzeug import secure_filename
app = Flask(__name__)
app.secret_key = 'nilas random string'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'snila@clustrex.com'
app.config['MAIL_PASSWORD'] = '********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


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


if __name__ == '__main__':
   app.run(debug = True)