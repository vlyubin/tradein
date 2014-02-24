from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    linkedin_id = db.Column(db.String(128), default='')
    publicUrl = db.Column(db.String(128), default='')
    authtoken = db.Column(db.String(256), default='')
    mail = db.Column(db.String(256), default='')
    pictureUrl = db.Column(db.String(256), default='')
    name = db.Column(db.String(128), default='')

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  category = db.Column(db.String(20), default='')
  descAndTitle = db.Column(db.String(1100), default='')
  desc = db.Column(db.String(1024), default='')
  title = db.Column(db.String(32), default='')
  img1 = db.Column(db.String(64), default='/static/images/GreyTrade300x400.png')
  img2 = db.Column(db.String(64), default='/static/images/GreyTrade300x400.png')
  img3 = db.Column(db.String(64), default='/static/images/GreyTrade300x400.png')
  img4 = db.Column(db.String(64), default='/static/images/GreyTrade300x400.png')
  price = db.Column(db.String(128), default='Free')
  selltype = db.Column(db.Integer, default=0)
  view = db.Column(db.Integer, default=0)
  timestamp = db.Column(db.DateTime)

  def get_dict(obj):
    return {
            'id': obj.id,
            'title': obj.title,
            'category': obj.category,
            'desc': obj.desc,
            'price': obj.price,
            'selltype': obj.selltype,
            'view': obj.view,
            'img1': obj.img1,
            'img2': obj.img2,
            'img3': obj.img3,
            'img4': obj.img4,
           }
