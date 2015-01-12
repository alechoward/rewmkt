# sql.py - Create a SQLite3 table and populate it with data
import sqlite3
# create a new database if the database doesn't already exist
with sqlite3.connect("blog.db") as connection:
# get a cursor object used to execute SQL commands
	c = connection.cursor()
# create the table 
	# c.execute ("""CREATE TABLE posts
	# (title TEXT, post TEXT, id INTEGER) 
	# """)


	# c.execute ("""CREATE TABLE users
	# (firstname TEXT, lastname TEXT, password TEXT, email TEXT, id INTEGER PRIMARY KEY) 
	# """)
# insert dummy data into the table
	#c.execute('INSERT INTO posts VALUES("Good", "I\'m good.", 1)') 
	# c.execute('INSERT INTO posts VALUES("Well", "I\'m well.", 1)') 
	# c.execute('INSERT INTO posts VALUES("Excellent", "I\'m excellent.", 0)')
	# c.execute('INSERT INTO posts VALUES("Okay", "I\'m okay.", 0)')

	#c.execute ("""CREATE TABLE products
	#(id INTEGER PRIMARY KEY, title TEXT, description TEXT, price INTEGER, url TEXT, points INTEGER) 
	#""")

	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("Fire HD 6","The Fire HD 6 goes anywhere with its pocketable design featuring a beautiful 6 inch HD display, 2x faster quad-core processor, and unsurpassed reliability in its class.",99,"img/items/item1.jpg",1000)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("$100 Amazon Gift Card","Purchase anything you would like on Amazon.com!",100,"img/items/item1.jpg",1000)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("Cuisinart Griddler","Compact in size but big in features, Cuisinarts countertop Griddler offers five-in-one functionality as a contact grill, panini press, full grill, full griddle and half grill/half griddle.",93,"img/items/item1.jpg",930)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("GoPro","GoPros high end camera model that features a new design with an integrated LCD, significantly increasing ease of use.",399,"img/items/item1.jpg",4000)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("Samsung Curved 48 Inch 1080p 240Hz 3D Smart LED TV","One of the best TVs on the market!",1300,"img/items/item1.jpg",13000)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("Nespresso Espresso Maker","Conceived to please both enthusiasts of Nespresso and lovers of modern design, Citiz is the expression of the union between high tech and retro-modern design inspirations. Nespresso began more than 25 years ago with a simple but revolutionary idea, to create the perfect cup of Espresso coffee with exquisite crema, tantalizing aroma and full bodied taste - just like skilled baristas.",179,"img/items/item1.jpg",1800)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("Uber Skis","Custom made, Uber branded high quality skis from <NAME>",400,"img/items/item1.jpg",4000)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("Uber Bicycle","Created by NAME, this bicycle is the best way (besides riding in an Uber!) to get around your city in style",800,"img/items/item1.jpg",8000)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("Uber CEO: A day in the life","Redeem these points for a day with TK getting an inside scoop on what life is like for a CEO",10000,"img/items/item1.jpg",150000)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("Workation","Work out of any Uber office in the world for 1 week, flight and housing paid for!",3000,"img/items/item1.jpg",30000)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("Uber Patagonia","Stay warm and look fresh in an Uber Patagonia!",180,"img/items/item1.jpg",1800)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("Bowflex Adjustable Dumbbells","Keep fit for Uber tank season with Bowflex adjustable Dumbbells",399,"img/items/item1.jpg",4000)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("LifeSpan TR 1200i Folding Treadmill","The LifeSpan TR1200i folding treadmill is durable, reliable, and loaded with valuable features, helping you walk, jog, or run with confidence in the comfort of your own home.",1000,"img/items/item1.jpg",10000)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("Yamaha Portable Grand Piano","If you are looking for a reasonably priced piano replacement, look no further than the YPG 235. It is the music student or professional musicians answer to I need more keys! and many music teachers encourage new students to get a keyboard that will grow with their needs.",280,"img/items/item1.jpg",2800)')
	# c.execute('INSERT INTO products(title, description, price, url, points) VALUES("Donation to Red Cross","Donate your points to the red cross",500,"img/items/item1.jpg",5000)')

	# c.execute ("""CREATE TABLE transactions
	# (transid INTEGER PRIMARY KEY, userid integer, applied_by_id integer, type text, description text, amount integer) 
	# """)

	# c.execute('INSERT INTO transactions(userid, applied_by_id, type, description, amount) VALUES (2, 1, "admin", "yearly account credits", 5000)')
	# c.execute('INSERT INTO transactions(userid, applied_by_id, type, description, amount) VALUES (3, 1, "admin", "yearly account credits", 5000)')
	

	# c.execute ("""CREATE TABLE balances
	# (userid integer, balance integer, updated_at date) 
	# """)

	# c.execute('INSERT INTO balances(userid, balance, updated_at) VALUES (2,5000,CURRENT_TIMESTAMP)')
	# c.execute('INSERT INTO balances(userid, balance, updated_at) VALUES (3,5000,CURRENT_TIMESTAMP)')

	# c.execute ("""CREATE TABLE balances
	# (id INTEGER PRIMARY KEY, userid integer, giftbalance integer, updated_at date, conid inte) 
	# """)

	#c.execute ("""ALTER TABLE gifttbalances ADD COLUMN id INTEGER PRIMARY KEY""")

	# c.execute ("""CREATE TABLE gifttbalances
	# (id INTEGER PRIMARY KEY, userid integer, giftbalance integer, updated_at date, conid integer) 
	# """)
	
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Uber Tank Top","Rep Uber with your guns out. Not included is the bullhorn you will need to fend your admirers away.",100,"img/items/ubertank.jpg",10)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Uber Credit: $50","Because there is no such thing as too much Uber credit. ",500,"img/items/ubercredit.jpg",50)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Amazon Gift Card: $50","Purchase anything you want from Amazon.com!",500,"img/items/amazon.jpg",50)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Donation to UNICEF","For those who prefer to pay it forward, you can use your Props to donate to a great cause.",500,"img/items/unicef.jpg",50)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Sephora Gift Card: $50","Give your skin care collection the revitalization it deserves.",500,"img/items/sephora.jpg",50)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Birchbox Subscription","Groom yourself with this 3 month subscription. Get new samples to gussy yourself up each month.",600,"img/items/birchbox.jpg",60)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Lululemon Yoga Mat","Time to destress in a way that does not affect your liver. Namaste. ",600,"img/items/lululemon.jpg",60)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Graze Subscription","Ten delicious boxes of healthy snacks. It will be difficult not to devour each box in one sitting.",700,"img/items/graze.jpg",70)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Cuisinart Griddler","You brought home the bacon with that project, now griddle it. ",1000,"img/items/griddler.jpg",100)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Fire HD 6","The Fire HD 6 goes anywhere with its pocketable design, featuring a beautiful 6 inch HD display, and 2x faster quad core processor.",1000,"img/items/firehd.jpg",100)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("CB2 Gift Card: $50","Find that rug that really brings the room together. Classy houseware and furniture that lets you finally replace that broken IKEA coffee table everyone and their mother has in their living room.",1000,"img/items/cb2.jpg",100)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Nespresso Espresso Maker","Whip up an espresso from the comfort of your own home, and avoid the barista sass. You can still spell the name wrong on your cup, if you prefer.",1800,"img/items/nespresso.jpg",180)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Uber Patagonia","Stay warm and look fresh in an Uber PataGucci!",1800,"img/items/patagonia.jpg",180)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Yamaha Portable Grand Piano","Hey there, Mister Piano Man! Whether you are a professional or hobbyist, this keyboard will grow with your needs.",2800,"img/items/piano.jpg",280)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("GoPro","Capture indoor, outdoor, under water, or base of a Fireball bottle action! The GoPro high end camera model features a new design with an integrated LCD, significantly increasing ease of use.",4000,"img/items/gopro.jpg",400)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Uber Skis","Custom made, Uber branded high quality skis from Icelantic.",4000,"img/items/skis.jpg",400)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Bowflex Adjustable Dumbbells","Keep fit for Uber tank season with Bowflex adjustable Dumbbells.",4000,"img/items/dumbells.jpg",400)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Uber Props shirt","Show your fellow Uber friends how awesome you are by strutting your stuff in a custom UberProps shirt!",8000,"img/items/propsshirt.jpg",800)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Samsung Curved 48 in TV","With 3D capability, this 1080p LED Smart TV makes it feel like you could touch the stubble on the chin of Daniel Radcliffe.",13000,"img/items/samsungtv.jpg",1300)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Workation ","Work out of any Uber office in the world for 1 week. Flight and housing paid for!",30000,"img/items/workation.jpg",3000)')
	c.execute('INSERT INTO products(title,description,points,url,price) VALUES ("Uber CEO: A day in the life","Redeem these points for a day with TK getting an inside scoop on what life is like for a CEO.",50000,"img/items/ceo.jpg",5000)')