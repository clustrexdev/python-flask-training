from flask import Flask, redirect, url_for, request
app = Flask(__name__)

## Routing and variable rules
@app.route('/')
def init():
   return 'Welcome to python programming'

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

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

if __name__ == '__main__':
   app.run(debug = True)