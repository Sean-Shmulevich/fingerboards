import time
import os
import json
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from models import db, User, Item, Order, Img

TODOS = {
	"todo1": {"task": "build an API", "done": True},
	"todo2": {"task": "?????", "done": False},
	"todo3": {"task": "profit!", "done": False},
}

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
	return rv.message_id if rv else None

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter_by(user_id=session['user_id']).first()

#homepage displays information about company and stuff this is basically entirely a static page
@app.route('/')
def homepage():
    return render_template('upload.html')

@app.route("/cart")
def cart():
    return render_template('cart.html',items=TODOS)

@app.route('/fetchItem/<item_id>',methods=["GET"])
def fetchItem(item_id=None):
    item = Item.query.filter_by(item_id=item_id).first()
    x = {
        f"item{item_id}": {"name": f"{item.item_name}", "price": f"{item.item_price}"}
    }
    return x

@app.route('/shop/<item>/addToCart',methods=["POST"])#this url should go to item own link
def addToCart(item):
    #add protections here
    '''
        req_data = request.get_json()
        print(req_data)

        id = int(max(TODOS.keys()).lstrip("todo")) + 1
        id = f"todo{id}"

        TODOS[id] = {"task": req_data["task"], "done": False}

        return {id: TODOS[id]}, 201
    '''
    a = Item.query.filter_by(item_id=item).first()
    user = User.query.filter_by(user_id=session['user_id']).first()
    user.cartItems.append(a)
    #add to current user json
    print(user.cartItems)
    return redirect(url_for('shop'))

@app.route('/shop/<item>')
def getItem(item):
    return render_template('item.html',item=Item.query.filter_by(item_id=item).first())

@app.route('/shop')
def shop():
    #image = Img.query.first()
    #a = Item('a',"b","c")
    #db.session.add(a)
    #a.pictures.append(image)
    #db.session.commit()
    return render_template('shop.html',items=Item.query)

@app.route('/upload', methods=['POST'])
def upload_img():
    #more input filtering on the size and type of inputs
    #pic = request.files['pic']

    #if not pic:
    #    return render_template('upload.html',error="wrong")

    #filename = secure_filename(pic.filename)
    #mimetype = pic.mimetype
    #if not filename or not mimetype:
    #    return render_template('upload.html',error="wrong")

    #if Img.query.filter_by(name=filename).first() is not None:
    #    return render_template('upload.html',error="same image has been uploaded before")

    #img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    #db.session.add(img)
    #db.session.commit()

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
