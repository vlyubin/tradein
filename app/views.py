from flask import request, session
from flask import Flask, render_template, jsonify, request
from app import app, models, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

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
      return render_template("404.html")
  except:
    return render_template("404.html")

  prod = models.Product.query.get(int_id)
  if prod:
      return render_template("pdp.html", prod=prod)
  else:
      return render_template("404.html")

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
