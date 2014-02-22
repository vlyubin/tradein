from flask import request, session
from flask import Flask, render_template, jsonify, request
from app import app, models, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import os, json
from models import Product

@app.route('/add', methods = ['POST'])
def add_product():
  title = str(request.form.get('title'))
  desc = str(request.form.get('desc'))
  category = str(request.form.get('category'))
  price = str(request.form.get('price'))
  descAndTitle = title + ' ' + desc # I need this for search
  imgLink = request.form.get('imgLink')
  imgLink2 = request.form.get('imgLink2')
  imgLink3 = request.form.get('imgLink3')
  imgLink4 = request.form.get('imgLink4')
  prod = models.Product(title=title, desc=desc, descAndTitle=descAndTitle, userid='FakeSoFake', category=category, price=price, img1=imgLink, img2=imgLink2, img3=imgLink3, img4=imgLink4)
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

  prod = Product.query.get(int_id)
  if prod:
      return render_template("pdp.html", prod=prod)
  else:
      return render_template('404.html'), 404

@app.route('/sell/<id>')
def edit_sell(id=None):
  try:
    int_id = int(id)
    if int_id < 0:
      return render_template('404.html'), 404
  except:
    return render_template('404.html'), 404

  prod = Product.query.get(int_id)
  prod.type = 'edit';
  return render_template('sell.html', product=prod);

@app.route('/sell')
def sell():
  return render_template('sell.html', product={'type':'add'});
  
@app.route('/search/<query>', methods = ['GET'])
def search(query=None):
  query = str(query)
  products = db.session.query(Product).filter(Product.descAndTitle.like("%" + query + "%")).limit(100).all()

  product_list = []
  for prod in products:
    product_list.append(prod.get_dict())

  return render_template('search.html', query=query, products=product_list)

@app.route('/dashboard')
def dashboard():
	products = db.session.query(Product).limit(20).all()
	return render_template('dashboard.html', products=products)

@app.route('/')
@app.route('/index')
def index():
  products = db.session.query(Product).limit(20).all()
  return render_template('homepage.html', products=products)

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
    try:
      os.stat(upload_folder)
    except:
      os.mkdir(upload_folder)
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
