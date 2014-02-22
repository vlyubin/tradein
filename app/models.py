from app import db

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  userid = db.Column(db.String(33), default='')
  category = db.Column(db.String(20), default='')
  descAndTitle = db.Column(db.String(1100), default='')
  desc = db.Column(db.String(1024), default='')
  title = db.Column(db.String(32), default='')
  img1 = db.Column(db.String(64), default='/app/static/images/GreyTrade300x400.png')
  img2 = db.Column(db.String(64), default='/app/static/images/GreyTrade300x400.png')
  img3 = db.Column(db.String(64), default='/app/static/images/GreyTrade300x400.png')
  img4 = db.Column(db.String(64), default='/app/static/images/GreyTrade300x400.png')
  price = db.Column(db.String(128), default=0)
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
