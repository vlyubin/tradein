from app import db

class Product(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(64), index = True)
