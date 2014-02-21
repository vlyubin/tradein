from app import db

class Producr(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(64), index = True)
