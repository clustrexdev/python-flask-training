import settings
from flask import Flask, url_for, redirect, request
from api.static import result, success, form
app = Flask(__name__)

# Simple Route
@app.route('/')
def hello_world():
  return 'Hello World'

# Basic Re-direct example
@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect('/')
   else:
      return redirect(url_for('hello_guest', guest = name))

# multiple methods handling
@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success', name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success', name = user))

# import seperate route
app.add_url_rule('/<name>', view_func = success)
app.add_url_rule('/result', view_func = result)
app.add_url_rule('/showform', view_func = form)

if __name__ == '__main__':
   app.run(debug=True)
