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

@app.route('/')
@app.route('/index')
def index():
  return "Hello, World!"
