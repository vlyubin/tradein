from flask import request, session
from flask import Flask, render_template, jsonify, request
from app import app, models, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import os, json

@app.route('/add', methods = ['POST'])
def add_product():
  title = request.form.get('title')
  description = request.form.get('description')

  prod = models.Product(title=title, desc=description, userid='FakeSoFake')
  db.session.add(prod)
  db.session.commit()

  return "/product/" + str(prod.id)

@app.route('/product/<id>')
def product(id=None):
  try:
    int_id = int(id)
    if int_id == None or int_id < 0:
      return render_template('404.html'), 404
  except:
    return render_template('404.html'), 404

  prod = models.Product.query.get(int_id)
  if prod:
      return render_template("pdp.html", prod=prod)
  else:
      return render_template('404.html'), 404

@app.route('/sell')
def sell():
  return render_template('sell.html')

@app.route('/search', methods = ['POST'])
def search():
  return "TODO"

@app.route('/')
@app.route('/index')
def index():
    return render_template('homepage.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/img', methods=['GET', 'POST'])
def upload_file():
  upload_folder = app.config['UPLOAD_FOLDER'];
  if request.method == 'POST':
    file = request.files['image']
    if not file or '.' not in file.filename:
      return "ERROR";
    extension = file.filename.rsplit('.', 1)[1]
    if extension not in app.config['ALLOWED_EXTENSIONS']:
      return json.dumps({"error":"File extension not allowed"})
    filename = os.urandom(16).encode('hex') + "." + extension
    file.save(os.path.join(upload_folder, filename))
    return json.dumps({"file":os.path.join('/static/uploads', filename)})
  if request.method == 'GET':
    filename = request.form.get('filename')
    if not filename:
      return "ERROR";
    file = os.path.join(upload_folder, filename);
    if not os.path.isfile(file):
      return "ERROR";
    return app.send_static_file(file)
