from app import db

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_token = db.Column(db.String(128), default='')
  category = db.Column(db.String(20), default='')
  descAndTitle = db.Column(db.String(1100), default='')
  desc = db.Column(db.String(1024), default='')
  title = db.Column(db.String(32), default='')
  img1 = db.Column(db.String(64), default='')
  img2 = db.Column(db.String(64), default='')
  img3 = db.Column(db.String(64), default='')
  img4 = db.Column(db.String(64), default='')
  price = db.Column(db.Integer, default=0)
  selltype = db.Column(db.Integer, default=0)
  view = db.Column(db.Integer, default=0)

  def get_dict(obj):
    return {
            'id': obj.id,
            'title': obj.title,
            'category': obj.category,
            'desc': obj.desc,
            'price': obj.price,
            'selltype': obj.selltype,
            'view': obj.view,
           }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authtoken = db.Column(db.String(256), default='')
    mail = db.Column(db.String(256), default='')
    pictureUrl = db.Column(db.String(256), default='')
    name = db.Column(db.String(128), default='')
