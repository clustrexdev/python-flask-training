from flask import Flask, redirect, url_for, request, render_template
from flask_mail import Mail, Message
app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'snila@clustrex.com'
app.config['MAIL_PASSWORD'] = '********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
## Routing and variable rules
# @app.route('/')
# def index():
#    return render_template('hello.html')

@app.route('/hello/<user>')
def hello_name(user):
   return render_template('hello.html', name = user)

# @app.route('/addNumber/<int:number1><int:number2>')
# def getNum(number1, number2) :
#   return 'The Addition of your number is.. %s' %number1+number2


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
def success(name):
  return 'Hello %s' %name

@app.route('/login', methods = ['GET','POST'])
def login():
  if request.method == 'POST':
    user = request.form['nm']
    return redirect(url_for('success',name = user))
  else:
    user = request.args.get('nm')
    return redirect(url_for('success',name = user))

@app.route('/calculateScore/<int:score>')
def calculateScore(score):
   return render_template('score.html', marks = score)

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)

# @app.route("/")
# def index():
#    return render_template("index.html")

@app.route("/")
def index():
   msg = Message('Flask Mail Check', sender = 'nilas116@gmail.com', recipients = ['pram@clustrex.com','kavi@clustrex.com'])
   msg.body = "Hi I am sending this mail from Flask"
   mail.send(msg)
   return "Sent"

if __name__ == '__main__':
   app.run(debug = True)