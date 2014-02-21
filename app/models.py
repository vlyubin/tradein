from app import db

class Product(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  userid = db.Column(db.String(33), unique = True)
  category = db.Column(db.String(20))
  desc = db.Column(db.String(512))
  title = db.Column(db.String(32))
  img1 = db.Column(db.String(64), unique = True)
  img2 = db.Column(db.String(64), unique = True)
  img3 = db.Column(db.String(64), unique = True)
  img4 = db.Column(db.String(64), unique = True)
  price = db.Column(db.Integer)
  selltype = db.Column(db.Integer)
  view = db.Column(db.Integer)

