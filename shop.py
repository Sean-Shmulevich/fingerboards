import time
import os
import json
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import stripe

from models import db, User, Item, Order, Img

cartList = []

stripe.api_key = "sk_test_51Kkk2UIc2DOJZXPJTJr4i2WPZDqeG70bAi6Y2TA4hMCMXntld7ayUBNRQgck0sLGJtG09a0tXGMVGWUgarkCkX5C00S3vYYVY6"
YOUR_DOMAIN = 'http://127.0.0.1:5000'
# create our little application :)
app = Flask(__name__)

# configuration
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'shop.db')

app.config.from_object(__name__)
app.config.from_envvar('FINGERBOARD_SETTINGS', silent=True)

db.init_app(app)

if __name__ == '__main__':
    #db.create_all()

    #db.session.commit()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,port=port)
    # configuration

@app.cli.command('initdb')
def initdb_command():
   """Creates the database tables."""
   db.create_all()

   db.session.commit()
   print('Initialized the database.')


def get_user_id(username):
	"""Convenience method to look up the id for a username."""
	rv = User.query.filter_by(username=username).first()
	return rv.user_id if rv else None

def get_item_id(name):
	"""Convenience method to look up the id for a username."""
	rv = Item.query.filter_by(item_name=name).first()
	return rv.item_price if rv else None

def multiplyQuantity(item):
    itemT = Item.query.filter_by(item_id=item).first()
    if(session.get("cart_items").get(f"item{item}").get("quantity") == None):
        return itemT.item_price
    a = float(session.get("cart_items").get(f"item{item}").get("quantity"))
    return a * float(itemT.item_price)

def addToCart(item):
    print(request.get_json())
    updateCartSess(item_id=item)
    #after the first press theres nothing in this
    if(session.get("cart_items").get(f"item{item}") != None):
        return session.get("cart_items").get(f"item{item}")
    else:
        itemT = Item.query.filter_by(item_id=item).first()
        x = {f"item{item}": {"name": f"{itemT.item_name}", "price": f"{itemT.item_price}"}}
        return x

def get_price(ran):
    if(ran != None):
        cartDict = ran
        toSum = 0
        for key in cartDict:
            i = float(cartDict[f"{key}"]["price"])
            if(cartDict[f"{key}"].get("quantity") != None):
                j = int(cartDict[f"{key}"]["quantity"])
                for k in range(j):
                    toSum += i
            else:
                toSum += i
        return toSum
    else:
        return 0.00

def get_num_items(ran):
    if(ran != None):
        cartDict = ran
        toSum = 0
        for key in cartDict:
            if(cartDict[f"{key}"].get("quantity") != None):
                j = int(cartDict[f"{key}"]["quantity"])
                for k in range(j):
                    toSum += 1
            else:
                toSum += 1
        return toSum
    else:
        return 0

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter_by(user_id=session['user_id']).first()

#homepage displays information about company and stuff this is basically entirely a static page
@app.route('/')
def homepage():
    return render_template('upload.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    print("here")
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1KkkI4Ic2DOJZXPJCZqU8Hb6',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url, code=303)

@app.route("/cart", methods=["GET","POST"])
def cart():
   print(session.get("cart_items"))
   if(request.method == "POST"):
       dictx = session.get("cart_items")
       print(request.form)
       if dictx:
           if 'dec' in request.form:
               updateItem = Item.query.filter_by(item_id=request.form["dec"])
               quant = int(request.form[f"cart{request.form['dec']}"])
               #request.form[f"cart{request.form['inc']}"] = quant+1
               if(quant == 1):
                   dictx[f"item{request.form['dec']}"]["quantity"] = 1
               else:
                   dictx[f"item{request.form['dec']}"]["quantity"] = quant-1
           elif 'inc' in request.form:
               print(request.form['inc'])
               quant = int(request.form[f"cart{request.form['inc']}"])
               dictx[f"item{request.form['inc']}"]["quantity"] = quant+1
           elif 'del' in request.form:
               dictx.pop(f"item{request.form['del']}")
           elif 'checkout' in request.form:
               create_checkout_session()
           session["cart_items"] = dictx

   jason = session.get("cart_items")
   cartList = []
   if(not jason):
       return render_template('cart.html')
   for key in jason:
      keyNum = int(key.replace("item",""))
      cartList.append(Item.query.filter_by(item_id=keyNum).first())
   return render_template('cart.html',items=cartList)

@app.route('/shop/<item_id>',methods=["POST"])
def updateCartSess(item_id=None):
    item = Item.query.filter_by(item_id=item_id).first()
    #okay so the problem is that after the refresh the price cart is not updated
    #the quantity is not updating after refresh first button press
    #after refresh session will not update itll stay the same why the fuck
    x = {f"item{item_id}": {"name": f"{item.item_name}", "price": f"{item.item_price}","quantity": "1"}}
    if(session.get("cart_items") == None):
        session["cart_items"] = x
    else:
        dictx = session.get("cart_items");
        if(dictx.get(f"item{item_id}") != None):
            newQuan = int(dictx[f"item{item_id}"]["quantity"])
            dictx[f"item{item_id}"] = {"name": f"{item.item_name}", "price": f"{item.item_price}", "quantity":f"{newQuan+1}"}
            session['cart_items'] = dictx
        else:
            dictx[f"item{item_id}"] = {"name": f"{item.item_name}", "price": f"{item.item_price}","quantity": "1"}
            session['cart_items'] = dictx
    return redirect(url_for("getItem", item=item_id))

@app.route('/fetchItem/<item_id>')
def getItemFast(item_id=None):
    #updateCartSess(item_id)
    return session.get("cart_items").get(f"item{item_id}")

@app.route('/shop/<item>',methods=["GET"])
def getItem(item):
    return render_template('item.html',item=Item.query.filter_by(item_id=item).first())

@app.route('/shop')
def shop():
    return render_template('shop.html',items=Item.query)

@app.route('/upload', methods=['POST'])
def upload_img():
    newItem = Item(request.form["name"],request.form["price"],request.form["description"])
    #newItem.pictures.append(img)
    db.session.add(newItem)
    db.session.commit()
    flash("sucessfully uploaded")
    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Logs the user in."""
	if g.user:
		return redirect(url_for('homepage'))
	error = None
	if request.method == 'POST':

		user = User.query.filter_by(username=request.form['username']).first()

		if request.form['username'] == "owner" and request.form['password'] == "pass":
			flash('Welcome owner')
			owner = True
			return redirect(url_for('login'))
		if user is None:
			error = 'Invalid username'
		elif not check_password_hash(user.pw_hash, request.form['password']):
			error = 'Invalid password'
		else:
			flash('You were logged in')
			session['user_id'] = user.user_id
			return redirect(url_for('homepage'))
	return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Registers the user."""
	if g.user:
		return redirect(url_for('homepage'))
	error = None
	if request.method == 'POST':
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['password']:
			error = 'You have to enter a password'
		elif request.form['password'] != request.form['password2']:
			error = 'The two passwords do not match'
		elif get_user_id(request.form['username']) is not None:
			error = 'The username is already taken'
		else:
			db.session.add(User(request.form['username'], generate_password_hash(request.form['password'])))
			db.session.commit()
			flash('You were successfully registered and can login now')
			return redirect(url_for('login'))
	return render_template('register.html', error=error)


@app.route('/logout')
def logout():
	"""Logs the user out."""
	flash('You were logged out')
	session.pop('user_id', None)
	return redirect(url_for('login'))


app.jinja_env.filters['getPrice'] = get_price
app.jinja_env.filters['getNumItems'] = get_num_items
app.jinja_env.filters['getMult'] = multiplyQuantity
