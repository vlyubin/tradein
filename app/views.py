from flask import request, session
from flask import Flask, render_template, jsonify, request
from app import app, models, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

@app.route('/add')
def add_product():
  title = request.form.get('title')
  description = request.form.get('description')

  prod = models.Product(title=title, description=description)
  db.session.add(prod)
  db.session.commit()

  return "/product/" + str(prod.id)

@app.route('/product/<id>')
def sell():
  # Use the id to get product data from db
  return render_template('pdp.html')

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
