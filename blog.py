# blog.py - controller
# imports
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
from functools import wraps 
from flask.ext.mail import Message, Mail
import sqlite3 
import collections
from random import randint
import datetime
import re


# configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY='hard_to_guess'
mail = Mail()
app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'Uberprops@gmail.com'
app.config["MAIL_PASSWORD"] = 'alectheduck'

mail.init_app(app)
# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)
# function used for connecting to the database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'], timeout=30000)

def login_required(test): 
    @wraps(test)
    def wrap(*args, **kwargs):
            if 'logged_in' in session:
                return test(*args, **kwargs) 
            else:
                flash('You need to login first.')
                return redirect(url_for('login')) 
    return wrap



@app.route('/add', methods=['POST'])
@login_required
def add():
	title = request.form['title']
	post = request.form['post']
	if not title or not post:
		flash("All fields are required. Please try again.")
		return redirect(url_for('main'))
	else:
		g.db = connect_db()
		g.db.execute('insert into posts (title, post,id) values (?,?,?)',[request.form['title'], request.form['post'], session['user_id']])
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted!') 
		return redirect(url_for('main'))


@app.route('/pointtrans', methods=['POST']) 
@login_required
def pointtrans():

	post = request.form['description']
	points = int(request.form['mymultiselect'])
	gift_to = request.form['uid'] 
	print gift_to
	#print title
	concat = 'getuser('+gift_to+')'
	print concat
	if not post:
		flash("All fields are required. Please try again.")
		return redirect(url_for('getuser', user_id=gift_to))
	else:
		g.db = connect_db()
		results = g.db.execute('select balance from balances where userid = ? and updated_at = (select max(updated_at) from balances where userid = ?)',[session['user_id'],session['user_id']])
		bal = [dict(bal=row[0]) for row in results.fetchall()]
		print bal 
		curbal = bal[0]['bal']
		g.db.commit()
		g.db.close()
		if points > curbal:
			flash("Not enough props")
			return redirect(url_for('getuser', user_id=gift_to))
		else:
			transcon = randint(1,1000000000)
			
			#add credits to users acct
			g.db = connect_db()
			g.db.execute('insert into transactions (userid, applied_by_id, type, description, amount, conid) values (?,?,?,?,?,?)',[gift_to, session['user_id'],'add_points', post, points, transcon])
			g.db.commit()
			g.db.close()
			
			g.db = connect_db()
			gresults = g.db.execute('select giftbalance from gifttbalances where userid = ? and updated_at = (select max(updated_at) from gifttbalances where userid = ?)',[gift_to,gift_to])
			gbal = [dict(bal=row[0]) for row in gresults.fetchall()]
			gcurbal = gbal[0]['bal']
			gnew_bal = gcurbal + points
			timestamp = datetime.datetime.utcnow()

			g.db.commit()
			g.db.close()
			g.db = connect_db()

			g.db.execute('insert into gifttbalances (userid, giftbalance, updated_at, conid) values (?,?,?,?)',[gift_to, gnew_bal, timestamp, transcon])
			g.db.commit()
			g.db.close()
			#subtract credits from session users acct
			negp = points*-1
			new_bal = curbal + negp
			g.db = connect_db()
			g.db.execute('insert into transactions (userid, applied_by_id, type, description, amount, conid) values (?,?,?,?,?,?)',[session['user_id'], session['user_id'],'subtract_points', post, negp, transcon])
			g.db.execute('insert into balances (userid, balance, updated_at, conid, status) values (?,?,?,?,?)',[session['user_id'], new_bal, timestamp, transcon, 'n'])

			g.db.commit()
			g.db.close()
			#flash('New entry was successfully posted!') 
			# send email

			msg = Message('[ACTION REQUIRED] Uber Props Approval', sender='uberprops@gmail.com', recipients=['propsmanager@gmail.com'])
      		msg.body = """From: Hi Alec, Your employee was given Props! Here's Why:"%s"<Approve> OR <Reject> Please contact Props@uber.com with any questions. Thank you! Props@uber.com Team""" % (post)
      		mail.send(msg)
		return redirect(url_for('giveconfirm', transcon=transcon))



@app.route('/', methods=['GET', 'POST']) 
def login():
	error = None
	if request.method == 'POST':
		#add if true/false here
		try:
			g.db = connect_db()
			results = g.db.execute("""select id, email, password from users where lower(email) = ? and password = ?""",(request.form['username'].lower(), request.form['password']))
			users = [dict(id=row[0], email=row[1], password=row[2]) for row in results.fetchall()] 
			if users != []:
				print users 
				for p in users:
					print p['id']
					session['user_id'] = p['id']
		#endfor
				g.db.commit()
				g.db.close()
				session['logged_in'] = True
		
				return redirect(url_for('main'))
			else:
				error = 'Invalid Credentials. Please try again.' 
				return render_template('login.html', error=error)
		except:
			error = 'Invalid Credentials. Please try again.' 

	return render_template('login.html', error=error)


@app.route('/transactions') 
@login_required
def transactions():
	g.db = connect_db()
	#gift balance
	cur = g.db.execute('select giftbalance from gifttbalances where userid = ? and updated_at = (select max(updated_at) from gifttbalances where userid = ?)',[session['user_id'],session['user_id']])
	giftb = [dict(bal=row[0]) for row in cur.fetchall()] 
	gfb = giftb[0]['bal']
	#gift/received transactions

	gift_trans = g.db.execute(
		'select Z.transid, Z.type, Z.description, Z.giftbalance, Z.amount, date(Z.updated_at), Z.firstname, Z.lastname from ( \
			select t.transid, t.type, t.description, gb.giftbalance, amount, gb.updated_at, "Uber" as firstname, "Admin" as lastname \
			from transactions t \
			join gifttbalances gb on gb.conid = t.conid \
			where t.applied_by_id = ? and t.type = "purchase" \
			UNION \
			select t.transid, t.type, t.description, gb.giftbalance, amount, gb.updated_at, u.firstname, u.lastname \
			from transactions t \
			join gifttbalances gb on gb.conid = t.conid \
			join users u on u.id = t.applied_by_id \
			where t.userid = ? and t.type = "add_points") Z \
		order by Z.updated_at DESC', [session['user_id'],session['user_id']])

	gift_trans_d = [dict(amt=row[4], fname = row[6], lname = row[7], bal= row[3], des = row[2], date =row[5]) for row in gift_trans.fetchall()]
	#awarded/admin balance

	results = g.db.execute('select balance from balances where userid = ? and updated_at = (select max(updated_at) from balances where userid = ?)',[session['user_id'],session['user_id']])
	bal = [dict(bal=row[0]) for row in results.fetchall()]
	print bal 
	curbal = bal[0]['bal']

	neg_trans = g.db.execute('select t.type, t.amount, t.userid, b.balance, u.firstname, u.lastname, t.conid, t.description, b.updated_at, date(b.updated_at) from transactions t join (select t.userid, t.conid from transactions t where t.type = "add_points") Z on Z.conid = t.conid join users u on u.id = Z.userid join balances b on b.conid = t.conid where t.applied_by_id = ? and type = "subtract_points" order by b.updated_at desc',[session['user_id'],])
	neg_trans_t = [dict(amt=row[1], fname = row[4], lname = row[5], bal= row[3], des = row[7], date =row[9]) for row in neg_trans.fetchall()] 
	print neg_trans_t
	g.db.commit()
	g.db.close()
	return render_template('account.html', neg_trans=neg_trans_t, givebal=gfb, give_trans = gift_trans_d, mybal=curbal)

@app.route('/faq')
@login_required
def faq():
	return render_template('FAQ.html')

@app.route('/main') 
@login_required
def main():
	g.db = connect_db()
	cur = g.db.execute('select * from posts')
	posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()] 
	g.db.commit()
	g.db.close()
	return render_template('home.html', posts=posts)
#marketplace/products page
@app.route('/redeem') 
@login_required
def redeem():
	g.db = connect_db()
	bal = g.db.execute('select giftbalance from gifttbalances where userid = ? and updated_at = (select max(updated_at) from gifttbalances where userid = ?)',[session['user_id'],session['user_id']])
	giftb = [dict(bal=row[0]) for row in bal.fetchall()] 
	gfb = giftb[0]['bal']

	cur = g.db.execute('select * from products')
	products = [dict(id=row[0], title=row[1], description=row[2], url=row[4], points=row[5]) for row in cur.fetchall()] 
	g.db.commit()
	g.db.close()
	return render_template('redeem1.html', products=products, gfb=gfb)

#individual product page
@app.route('/redeem/<int:prod_id>/') 
@login_required
def getproduct(prod_id):
	
	prodid = prod_id
	g.db = connect_db()
	cur = g.db.execute("""select * from products where id = ?""",((prodid,)))
	product = [dict(id=row[0], title=row[1], des=row[2], img=row[4], points=row[5]) for row in cur.fetchall()] 

	bal = g.db.execute('select giftbalance from gifttbalances where userid = ? and updated_at = (select max(updated_at) from gifttbalances where userid = ?)',[session['user_id'],session['user_id']])
	giftb = [dict(bal=row[0]) for row in bal.fetchall()] 
	gfb = giftb[0]['bal']
	g.db.commit()
	g.db.close()
	return render_template('item-listing.html', product=product, gfb = gfb)


@app.route('/ordersummary/<int:prod_id>', methods=['GET','POST'])
@login_required
def purchase(prod_id):

	g.db = connect_db()
	bal = g.db.execute('select giftbalance from gifttbalances where userid = ? and updated_at = (select max(updated_at) from gifttbalances where userid = ?)',[session['user_id'],session['user_id']])
	giftb = [dict(bal=row[0]) for row in bal.fetchall()] 
	gfb = giftb[0]['bal']
	
	user = g.db.execute('select firstname, lastname, email from users where id = ?',[session['user_id'],])
	users = [dict(fname=row[0], lname=row[1], email=row[2]) for row in user.fetchall()] 
	cur = g.db.execute("""select * from products where id = ?""",((prod_id,)))
	product = [dict(id=row[0], title=row[1], des=row[2], img=row[4], points=row[5]) for row in cur.fetchall()] 
	pprice = product[0]['points']


	idprod = prod_id
	if pprice > gfb:
		flash("Not enough props")
		g.db.commit()
		g.db.close()
		return redirect(url_for('getproduct', prod_id=prod_id, user=users))
		
	else: 
		#product transaction logged on transactions table as purchase
		transcon = randint(1,1000000000)
		g.db.execute('insert into transactions (userid, applied_by_id, type, description, amount, conid) values (?,?,?,?,?,?)',[session['user_id'], session['user_id'],'purchase', product[0]['title'], pprice*-1, transcon])

		#update giftbalances after transaction
		gnew_bal = gfb - pprice
		
		timestamp = datetime.datetime.utcnow()
		g.db.execute('insert into gifttbalances (userid, giftbalance, updated_at, conid) values (?,?,?,?)',[session['user_id'], gnew_bal, timestamp, transcon])
		g.db.commit()
		g.db.close()
		
		return render_template('order-confirmation.html', product=product, gfb = gfb)


#search landing page
@app.route('/search') 
@login_required
def searchL():
	g.db = connect_db()
	#search = request.form['search-employees']
	results = g.db.execute('select balance from balances where userid = ? and updated_at = (select max(updated_at) from balances where userid = ?)',[session['user_id'],session['user_id']])
	bal = [dict(bal=row[0]) for row in results.fetchall()]
	curbal = bal[0]['bal']
	
	cur = g.db.execute("""select firstname, lastname, email, id from users where id != ? limit 10""",((int(session['user_id'])),))
	users = [dict(firstname=row[0], lastname=row[1], email=row[2], id=row[3]) for row in cur.fetchall()] 

	g.db.commit()
	g.db.close()
	return render_template('search.html', users=users, bal=curbal)

@app.route('/search1', methods=['POST'])
@login_required
def search1():
	text1 = request.form['search-employees']
	print text1
	#return render_template('search.html')
	return redirect(url_for('search123', text=text1))
	#return redirect(url_for('search123', text=text1))
#search for users to give points
@app.route('/search12/<text>', methods=['GET','POST']) 
@login_required
def search123(text):
	#text = request.form['search-employees']
	searchelem = re.sub("[^\w]", " ",  text).split()
	#print searchelem
	textr = '%' + text + '%'
	g.db = connect_db()
	cur = g.db.execute("""select * from users where firstname like ? or lastname like ? or email like ? """, (textr,textr,textr))
	users = [dict(firstname=row[0], lastname=row[1], email=row[3], id=row[4]) for row in cur.fetchall()] 
	
	#display current balance
	results = g.db.execute('select balance from balances where userid = ? and updated_at = (select max(updated_at) from balances where userid = ?)',[session['user_id'],session['user_id']])
	bal1 = [dict(bal=row[0]) for row in results.fetchall()]
	curbal1 = bal1[0]['bal']
	print curbal1

	g.db.commit()
	g.db.close()
	#print users
	return render_template('give-search-results.html', users=users, bal1=curbal1)


# give confimraiton page

@app.route('/giveconfirm/<transcon>') 
@login_required
def giveconfirm(transcon):

	g.db = connect_db()

	results = g.db.execute('select balance from balances where userid = ? and updated_at = (select max(updated_at) from balances where userid = ?)',[session['user_id'],session['user_id']])
	bal1 = [dict(bal=row[0]) for row in results.fetchall()]
	curbal1 = bal1[0]['bal']
	print transcon 
	cur = g.db.execute("""select description, amount, userid, u.firstname, u.lastname, u.mfirst, u.memail from transactions t join users u on u.id = t.userid where conid = ? and type = 'add_points'""",((transcon,)))
	giveconfirm = [dict(fname=row[3], lname=row[4], amt = row[1]) for row in cur.fetchall()]
	return render_template('give-confirmation.html', bal=curbal1, giveconfirm=giveconfirm)
# give points to another user

@app.route('/giveuser/<int:user_id>') 
@login_required
def getuser(user_id):
	new_id = user_id
	g.db = connect_db()
	cur = g.db.execute("""select firstname, lastname, email, id, mfirst, mlast, memail from users where id = ?""",((new_id,)))
	users = [dict(firstname=row[0], lastname=row[1], email=row[2], id=row[3], mfirst=row[4], mlast=row[5]) for row in cur.fetchall()] 

	results = g.db.execute('select balance from balances where userid = ? and updated_at = (select max(updated_at) from balances where userid = ?)',[session['user_id'],session['user_id']])
	bal1 = [dict(bal=row[0]) for row in results.fetchall()]
	curbal1 = bal1[0]['bal']
	print curbal1

	return render_template('give-award.html', users=users, bal = curbal1)


@app.route('/profile') 
@login_required
def profile():
	g.db = connect_db()
	print session['user_id']
	results = g.db.execute("""select id, email, password from users where id = ?""",((int(session['user_id'])),))
	users = [dict(id=row[0], email=row[1], password=row[2]) for row in results.fetchall()] 
	print session['user_id']
	g.db.commit()
	g.db.close()
	return render_template('profile.html', posts=users)

@app.route('/logout') 
def logout():
	session.pop('logged_in', None) 
	flash('You were logged out') 
	return redirect(url_for('login'))

if __name__ == '__main__': 
	app.run(debug=True)