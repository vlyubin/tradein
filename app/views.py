from flask import request, session
from flask import Flask, render_template, jsonify, request, redirect, url_for
from app import app, models, db
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
import os, json
from models import Product
from models import User
import urllib2
from xml.dom import minidom

#################################
# OAuth stuff
#################################

@app.before_first_request
def before_first_request():
		session['tradein_user_oauth_token'] = None
		session['tradein_user_oauth_secret'] = None

@app.route('/login')
def login():
	return redirect('https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=75c20ft4h4tqkc&scope=r_basicprofile%20r_emailaddress&state=wenfui2s8923fbiuASDASDYdn23diu23dbiu23bdn23oidb3y2vd3&redirect_uri=' + request.url_root + 'addtoken');

def create_or_update_user(token):
	try:
		info_request = 'https://api.linkedin.com/v1/people/~:(first-name,last-name,email-address,picture-url,id,public-profile-url)?oauth2_access_token=' + token
		info_response = urllib2.urlopen(info_request)
		xml_response = minidom.parse(info_response)
	except:
		return None

	firstName = xml_response.getElementsByTagName('first-name')[0].firstChild.nodeValue
	lastName = xml_response.getElementsByTagName('last-name')[0].firstChild.nodeValue
	email = xml_response.getElementsByTagName('email-address')[0].firstChild.nodeValue
	linkedin_id = xml_response.getElementsByTagName('id')[0].firstChild.nodeValue
	publicUrl = xml_response.getElementsByTagName('public-profile-url')[0].firstChild.nodeValue

	try:
		picture = xml_response.getElementsByTagName('picture-url')[0].firstChild.nodeValue
	except:
		picture = 'http://static02.linkedin.com/scds/common/u/img/icon/icon_no_photo_80x80.png' # User has no picture

	try:
		user = User.query.filter(User.linkedin_id == linkedin_id).one()
		user.authtoken = token # Update users token
	except: # Excpetion gets raised if no such user exists. Create one
		user = User(authtoken=token, mail=email, name=firstName + ' ' + lastName, pictureUrl=picture, linkedin_id=linkedin_id, publicUrl=publicUrl)

	db.session.add(user)
	db.session.commit()

	return user

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

def user_get():
	try:
		return User.query.filter(User.authtoken == str(session['tradein_user_oauth_token'])).one()
	except:
		return create_or_update_user(str(session['tradein_user_oauth_token'])) # It looks like the token wasn't recognized. Update it

def user_loggedin():
	return 'tradein_user_oauth_token' in session and session['tradein_user_oauth_token'] != ''

#################################
# Homepage
#################################

@app.route('/')
@app.route('/home')
@app.route('/index')
def page_index():
	products = db.session.query(Product).order_by(Product.timestamp.desc()).limit(20).all()
	for product in products:
		product.desc = " ".join(product.desc[:150].split(" ")[:-1]) + "..." if len(product.desc) > 150 else product.desc

	return render_template('homepage.html', products=products)

#################################
# Dashboard
#################################

@app.route('/dashboard')
def page_dashboard():
	if not user_loggedin():
		return redirect('/login')
	user = user_get()

	if user == None:
		return redirect('/login')

	products = db.session.query(Product).filter(Product.user_id == user.id)
	return render_template('dashboard.html', products=products, num_products=products.count())

#################################
# Search page
#################################

@app.route('/search/<query>', methods = ['GET'])
def page_search(query=None):
	query = str(query)
	products = db.session.query(Product).filter(Product.descAndTitle.like("%" + query + "%")).limit(100).all()
	for product in products:
		product.desc = " ".join(product.desc[:150].split(" ")[:-1]) + "..." if len(product.desc) > 150 else product.desc

	return render_template('search.html', query=query, products=products)

#################################
# Product page
#################################

@app.route('/product/<id>')
def page_product(id=None):
	try:
		int_id = int(id)
		if int_id == None or int_id < 0:
			return err404()
	except:
		return err404()

	product = db.session.query(Product).get(int_id)
	if product:
		user = db.session.query(User).get(product.user_id)

		product.view += 1 # We just viewed the product page
		db.session.add(product)
		db.session.commit()

		return render_template("pdp.html", prod=product, user=user)
	else:
		return err404()

#################################
# Sell and Edit page
#################################

@app.route('/sell')
def page_sell_new():
	if not user_loggedin():
		return redirect('/login')
	user = user_get()
	if user == None:
		return redirect('/login')

	return render_template('sell.html', product={'type':'add'});

@app.route('/sell/<id>')
def page_sell_edit(id=None):
	if not user_loggedin():
		return redirect('/login')
	user = user_get()
	if user == None:
		return redirect('/login')

	try:
		product_id = int(id)
		if product_id == None or product_id < 0:
			return err404()
	except:
		return err404()

	prod = Product.query.get(product_id)
	prod.type = 'edit';
	return render_template('sell.html', product=prod);

#################################
# AJAX Product handlers
#################################

@app.route('/add', methods = ['POST'])
def ajax_add_product():
	if not user_loggedin():
		return redirect('/login')
	user = user_get()
	
	product = save_product_from_request(user)

	return "/product/" + str(product.id)

@app.route('/edit/<id>', methods = ['POST'])
def ajax_edit_product(id=None):
	#Check login
	if not user_loggedin():
		return redirect('/login')
	user = user_get()

	if id == None or not id.isdigit():
		return err404()

	product_id = int(id)
	product = Product.query.get(product_id)

	# Someone try to modify item of other user, disallow!
	if product.user_id != user.id:
		return err404()
		
	product = save_product_from_request(user, product)
	return "/product/" + str(product.id)

@app.route('/remove/<id>', methods = ['POST'])
def ajax_remove_product(id=None):
	try:
		product_id = int(id)
		if product_id == None or product_id < 0:
			return err404()
	except:
		return err404()

	if not user_loggedin():
		return err404()
	user = user_get()

	try:
		product = Product.query.get(product_id)
	except:
		return err500()

	if product.user_id != user.id: # You are trying to delete a product that doesn't belong to you
		return render_template('500.html'), 500

	db.session.delete(product)
	db.session.commit()

	return "" # Means that everything went OK

def save_product_from_request(user, product=None):
	title = str(request.form.get('title'))
	desc = str(request.form.get('desc'))
	category = str(request.form.get('category'))

	# If we were passed a number, append a dollar sign to it
	try:
		float(str(request.form.get('price')))
		price = str(request.form.get('price')) + "$"
	except:
		price = str(request.form.get('price'))

	descAndTitle = title + ' ' + desc # Needed for search
	imglist = str(request.form.get('imglist'))
	imgcount = int(request.form.get('imgcount'))

	# Put at least one image
	if(imgcount == 0):
		imgcount = 1
		imglist = '/static/images/default.jpg'

	if product == None:
		product = Product(title=title, desc=desc, descAndTitle=descAndTitle, user_id=user.id, category=category, \
			price=price, imglist=imglist, imgcount=imgcount, timestamp=datetime.datetime.utcnow())
	else:
		product.title = title
		product.desc = desc
		product.descAndTitle = descAndTitle
		product.category = category
		product.price = price
		product.imglist = imglist
		product.imgcount = imgcount
		product.timestamp = datetime.datetime.utcnow()

	db.session.add(product)
	db.session.commit()
	return product


#################################
# AJAX User
#################################

@app.route('/user')
def get_current_user():
	if not user_loggedin():
		return jsonify(user='{}')

	user = user_get()
	if user == None:
		return jsonify(user='{}')

	return jsonify(user=user.serialize())


#################################
# Image upload
#################################

@app.route('/img', methods=['GET', 'POST'])
def image():
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

#################################
# Error handlers
#################################

@app.errorhandler(404)
def page_not_found(e):
	return err404()

@app.errorhandler(500)
def page_not_found(e):
	return err500()

def err404():
	return render_template('404.html'), 404

def err500():
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
