from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

orders = db.Table('orders',
	db.Column('order_name', db.Integer, db.ForeignKey('order.name')),
	db.Column('user_user_id', db.Integer, db.ForeignKey('user.user_id')),
)

class Order(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.Integer)
   item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)

   def __init__(self, name,item_id):
      self.name = name
      self.item_id = item_id

   def __repr__(self):
      return '<Purchase {}>'.format(self.name)

items = db.Table('items',
	db.Column('item_id', db.Integer, db.ForeignKey('item.item_id')),
	db.Column('user_user_id', db.Integer, db.ForeignKey('user.user_id')),
)

class User(db.Model):
   user_id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(24), nullable=False)
   pw_hash = db.Column(db.String(64), nullable=False)

#purchase = db.relationship('Order', backref='buyer')

   orders = db.relationship('Order', secondary=orders, backref=db.backref('users', lazy='dynamic'))
   cartItems = db.relationship('Item', secondary=items, backref=db.backref('cartUser', lazy='dynamic'))

   def __init__(self, username, pw_hash):
      self.username = username
      self.pw_hash = pw_hash

   def __repr__(self):
      return '<User {}>'.format(self.username)

images = db.Table('images',
	db.Column('img_id', db.Integer, db.ForeignKey('img.id')),
	db.Column('item_item_name', db.Integer, db.ForeignKey('item.item_name')),
)

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(24), nullable=False)
    item_price = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(24), nullable=False)

    pictures = db.relationship('Img', secondary=images, backref=db.backref('pics', lazy='dynamic'))
    itemOrdered = db.relationship('Order', backref='item')

    def __init__(self, item_name, item_price, description):
        self.item_name = item_name
        self.item_price = item_price
        self.description = description

    def __repr__(self):
        return '<Item {}>'.format(self.item_name)
##user has an event associated with it with backref author
##user has a table of days that they are working
##event has three people assoicated with it.
'''
class Order(db.Model):
   order_id = db.Column(db.Integer, primary_key=True)
   #buyer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
   item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
   #pub_date = db.Column(db.String(24), nullable=False)
   #tracking = db.Column(db.String(24), nullable=False)
   #messages = db.relationship('User', backref='message')


   def __init__(self, item_id):
      self.item_id = item_id


   def __repr__(self):
      return '<Order {}'.format(self.order_id)
'''
