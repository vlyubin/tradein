from flask import request, session
from flask import Flask, render_template, jsonify, request, redirect, url_for
from app import app, models, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import os, json
from models import Product
import urllib2

@app.before_first_request
def before_first_request():
    session['user_oauth_token'] = None
    session['user_oauth_secret'] = None

@app.route('/sessiontest')
def sessiontest():
  if 'tradein_user_oauth_token' in session:
    token = session['tradein_user_oauth_token']
    if token == '':
      return "ABSENT"
    return session['tradein_user_oauth_token']
  return "ABSENT"

@app.route('/login')
def login():
  #
  # WARNING WARNING DANGER DANGER Return adress is hardcoded
  #
  return redirect('https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=75c20ft4h4tqkc&scope=r_fullprofile%20r_emailaddress&state=wenfui2s8923fbiuASDASDYdn23diu23dbiu23bdn23oidb3y2vd3&redirect_uri=http://127.0.0.1:5000/addtoken');

@app.route('/addtoken')
def addtoken():
  #
  # WARNING WARNING DANGER DANGER Return adress is hardcoded
  #
  code = request.args.get('code', '')
  response = urllib2.urlopen('https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code&code=' + code + '&redirect_uri=http://127.0.0.1:5000/addtoken&client_id=75c20ft4h4tqkc&client_secret=ZPYvP8NPtMRuYB4l')
  obj = json.loads(response.read())

  key = obj.get('access_token')
  session['tradein_user_oauth_token'] = key
  session['tradein_user_oauth_secret'] = 'f0973ff4-1689-4c1c-87df-f70781755e09'

  # Query users data from LinkedIn and create db entry for them
  names_request = 'https://api.linkedin.com/v1/people/~:(first-name,last-name)?oauth2_access_token=' + session['tradein_user_oauth_token']
  names_response = urllib2.urlopen(names_request)
  names_html = names_response.read()

  mail_request = 'https://api.linkedin.com/v1/people/~:(email-address,picture-url)?oauth2_access_token=' + session['tradein_user_oauth_token']
  mail_response = urllib2.urlopen(mail_request)
  mail_html = mail_response.read()
  mail_and_pict = mail_html.split(' ')

  user = models.User(authtoken=key, mail=mail_and_pict[0], name=names_html, pictureUrl=mail_and_pict[1])
  db.session.add(user)
  db.session.commit()

  return redirect('/sell') # return to sell page

# OAuth stuff ends

@app.route('/add', methods = ['POST'])
def add_product():
  title = str(request.form.get('title'))
  desc = str(request.form.get('desc'))
  category = str(request.form.get('category'))
  price = str(request.form.get('price'))
  descAndTitle = title + ' ' + desc # I need this for search
  imgLink = request.form.get('imgLink')
  prod = models.Product(title=title, desc=desc, descAndTitle=descAndTitle, user_token=str(session['tradein_user_oauth_token']), category=category, price=int(price), img1=imgLink)
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

@app.route('/sell')
def sell():
  # Redirect to login if no token
  if not 'tradein_user_oauth_token' in session or session['tradein_user_oauth_token'] == '':
    return redirect('/login')
  return render_template('sell.html')

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
  return render_template('dashboard.html')

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
