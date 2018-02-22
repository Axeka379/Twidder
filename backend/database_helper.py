import sqlite3
from flask import g



my_db = 'database.db'

#connect to database
def connect_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(my_db)
	return db

#closes database when teardown
@app.teardown_appcontext
def close_connection_db(exception):
	db = getattr(g, '_database', None)
	if fb is not None:
		db.close()

def query_db(query, args=(), one=False):
	cursor = connect_db().execute(query, args)
	result = cursor.fetcall()
	cursor.close()
	return (result[0] if result else None) if one else result


#insert a user into the database
def insert_user(): #lägg till parametrar (prob json)
	connect = connect_db()

	cursor = connect.cursor()
	cursor.execute('''INSERT INTO users(email,firstname,familyname,password,sex,city,country,token)
						VALUES(?,?,?,?,?,?,?,?)''', (email, firstname, familyname, password, sex, city, country, token))
	connect.commit()
	#close cursor ???
	return cursor.lastrowid

#find a user from the database
def find_user(): #lägg till parametrar
	user = query_db('select * from users where email = ?',
				[email], one=true)
	if user is None: #Change to json message, success = false and so on
		print ('Couldn\'t find user')
	else:
		print ('found the user', user['email'])
	return user #kan behöva ändras. Vad är user exakt?


def remove_user(): #lägg till parametrar
	connect = connect_db()

	cursor = connect.cursor()
	cursor.execute('''DELETE FROM users WHERE email =?''', (email))
	connect.commit()
	#close cursor ???
	return cursor.lastrowid

def create_post(): #lägg till parametrar
	connect = connect_db()
	cursor.execute('''INSERT INTO messages(sender, message, receiver)
						VALUES(?,?,?)''', (email1, text, email2))
	connect.commit()
	#close cursor ???
	return cursor.lastrowid
