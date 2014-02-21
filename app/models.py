from app import db

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  userid = db.Column(db.String(33), default='')
  category = db.Column(db.String(20), default='')
  desc = db.Column(db.String(512), default='')
  title = db.Column(db.String(32), default='')
  img1 = db.Column(db.String(64), default='')
  img2 = db.Column(db.String(64), default='')
  img3 = db.Column(db.String(64), default='')
  img4 = db.Column(db.String(64), default='')
  price = db.Column(db.Integer, default=0)
  selltype = db.Column(db.Integer, default=0)
  view = db.Column(db.Integer, default=0)
