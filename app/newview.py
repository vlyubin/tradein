from flask import request, session
from flask import Flask, render_template, jsonify, request
from app import app, models, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

@app.route('/add', methods = ['POST'])
def add_product():
  title = request.form.get('title')
  description = request.form.get('description')
  category = request.form.get('category')
  price = request.form.get('price')
  selltype = request.form.get('selltype')
  prod = models.Product(title=title, desc=description, userid='FakeSoFake',category=price,selltype=selltype)
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

@app.route('/search/<query>', methods = ['POST'])
def search():
  products = db.session.query(models.Product).limit(20).all()

  product_list = []
  for prod in products:
    product_list.append({'three': 3, 'one': 1, 'two': 2})

  return jsonify(products=product_list)

@app.route('/')
@app.route('/index')
def index():
  products = db.session.query(models.Product).limit(20).all()
  return render_template('homepage.html', products=products)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
  return render_template('500.html'), 500