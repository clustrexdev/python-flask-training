import os
from flask import render_template, request

def success(name):
  return render_template('welcome.html', name=name, app_name=os.getenv('app_name'))

def form():
  return render_template('form.html')

def result():
  dict = {}
  if request.method == 'POST':
    dict = request.form
  else:
    dict = {'phy':50,'che':60,'maths':70}
  return render_template('result.html', result = dict)
