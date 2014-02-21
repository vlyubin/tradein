<<<<<<< HEAD
from flask import request, session
from flask import render_template, make_response
from app import app, models, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

def add_product():
  return "TODO"

@app.route('/product')
def sell():
  return "TODO"

@app.route('/sell')
def sell():
  return "TODO"

@app.route('/search')
def search():
  return "TODO"
=======
from app import app
from flask import Flask, render_template, jsonify, request

>>>>>>> e4d201f3a4a836ea3f2b1cf26971e8325876b66c

@app.route('/')
@app.route('/index')
def index():
<<<<<<< HEAD
  return "Hello, World!"
=======
    return render_template('homepage.html')
>>>>>>> e4d201f3a4a836ea3f2b1cf26971e8325876b66c
