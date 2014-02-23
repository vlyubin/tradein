from flask import request, session
from flask import Flask, render_template, jsonify, request, redirect, url_for
from app import app, models, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import os, json
from models import Product
from models import User
import urllib2
from xml.dom import minidom

#
# OAuth stuff begins
#
@app.before_first_request
def before_first_request():
    session['user_oauth_token'] = None
    session['user_oauth_secret'] = None

@app.route('/login')
def login():
  return redirect('https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=75c20ft4h4tqkc&scope=r_basicprofile%20r_emailaddress&state=wenfui2s8923fbiuASDASDYdn23diu23dbiu23bdn23oidb3y2vd3&redirect_uri=' + request.url_root + 'addtoken');

def create_or_update_user(token):
  info_request = 'https://api.linkedin.com/v1/people/~:(first-name,last-name,email-address,picture-url,id)?oauth2_access_token=' + token
  info_response = urllib2.urlopen(info_request)
  xml_response = minidom.parse(info_response)

  firstName = xml_response.getElementsByTagName('first-name')[0].firstChild.nodeValue
  lastName = xml_response.getElementsByTagName('last-name')[0].firstChild.nodeValue
  email = xml_response.getElementsByTagName('email-address')[0].firstChild.nodeValue
  linkedin_id = xml_response.getElementsByTagName('id')[0].firstChild.nodeValue

  try:
    picture = xml_response.getElementsByTagName('picture-url')[0].firstChild.nodeValue
  except:
    picture = 'http://static02.linkedin.com/scds/common/u/img/icon/icon_no_photo_80x80.png' # User has no picture

  try:
    user = User.query.filter(User.linkedin_id == linkedin_id).one()
    user.authtoken = token # Update users token
  except: # Excpetion gets raised if no such user exists. Create one
    user = User(authtoken=token, mail=email, name=firstName + ' ' + lastName, pictureUrl=picture, linkedin_id=linkedin_id)

  db.session.add(user)
  db.session.commit()

@app.route('/addtoken')
def addtoken():
  code = request.args.get('code', '')
  response = urllib2.urlopen('https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code&code=' + code + '&redirect_uri=' + request.url_root + 'addtoken&client_id=75c20ft4h4tqkc&client_secret=ZPYvP8NPtMRuYB4l')
  obj = json.loads(response.read())

  key = obj.get('access_token')
  session['tradein_user_oauth_token'] = key
  session['tradein_user_oauth_secret'] = 'f0973ff4-1689-4c1c-87df-f70781755e09'

  create_or_update_user(key)

  return redirect('/sell') # redirect to sell page
#
# OAuth stuff ends
#

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

  if not 'tradein_user_oauth_token' in session or session['tradein_user_oauth_token'] == '':
    return redirect('/login')
  try:
    user = User.query.filter(User.authtoken == str(session['tradein_user_oauth_token'])).one()
  except:
    user = create_or_update_user(str(session['tradein_user_oauth_token'])) # It looks like the token wasn't recognized. Update it

  prod = models.Product(title=title, desc=desc, descAndTitle=descAndTitle, user_id=user.id, category=category, price=price, img1=imgLink, img2=imgLink2, img3=imgLink3, img4=imgLink4)

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

@app.route('/remove/<id>')
def remove(id=None):
  try:
    int_id = int(id)
    if int_id < 0:
      return render_template('404.html'), 404
  except:
    return render_template('404.html'), 404

  prod = Product.query.get(int_id)

  return redirect('/dashboard')

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
  # Redirect to login if no token
  if not 'tradein_user_oauth_token' in session or session['tradein_user_oauth_token'] == '':
    return redirect('/login')
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
  # Redirect to login if no token
  if not 'tradein_user_oauth_token' in session or session['tradein_user_oauth_token'] == '':
    return redirect('/login')

  try:
    user = User.query.filter(User.authtoken == str(session['tradein_user_oauth_token'])).one()
  except:
    user = create_or_update_user(str(session['tradein_user_oauth_token'])) # It looks like the token wasn't recognized. Update it

  products = db.session.query(Product).filter(Product.user_id == user.id)
  return render_template('dashboard.html', products=products)

@app.route('/')
@app.route('/index')
def index():
  products = db.session.query(Product).limit(20).all()
  return render_template('homepage.html', products=products)

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

# Error handlers

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
  return render_template('500.html'), 500

# Debug helpers, remove when development is done
@app.route('/sessiontest')
def sessiontest():
  if 'tradein_user_oauth_token' in session:
    token = session['tradein_user_oauth_token']
    if token == '':
      return "ABSENT"
    return session['tradein_user_oauth_token']
  return "ABSENT"
