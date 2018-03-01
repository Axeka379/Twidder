from flask import Flask
import sqlite3
from flask import g

DATABASE = './database.db'
#/home/malbr878/TDDD97/backend/database.db



#connect to database
def connect_db():
	print("Connected")
	g.db = sqlite3.connect(DATABASE)




#closes database
def close_connection_db():
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()



def query_db(query, args=(), one=False):
	cursor = connect_db().execute(query, args)
	result = cursor.fetcall()
	cursor.close()
	return (result[0] if result else None) if one else result




#insert a user into the database
def insert_user(email, firstname, familyname, password, sex, city, country):
	#do we need this? result = []

	try:
		cursor = g.db.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?)" , [email, firstname, familyname, password, sex, city, country, ""])
		g.db.commit()

		return True
	except:
		return False



#find a user from the database
def find_user(email):
	result = []
	cursor = g.db.execute("select * from users where email = ?", [email])
	#commit
	rows = cursor.fetchall()
	cursor.close()
	for index in range(len(rows)):
		result.append({'email':rows[index][0], 'firstname':rows[index][0],
			'familyname':rows[index][0], 'password':rows[index][0],
			'sex':rows[index][0], 'city':rows[index][0],
			'country':rows[index][0], 'token':rows[index][0]})
	return result




def remove_user(email):
	connect = connect_db()

	cursor = g.db.execute("DELETE FROM users WHERE email =?", [email])
	g.db.commit()
	return cursor.lastrowid



def create_post(sender, message, receiver):
	#do we need this? result = []
	try:
		cursor = g.db.execute("INSERT INTO messages VALUES(?,?,?)" , [sender, message, receiver])
		g.db.commit()
		return True
	except:
		return False



def update_password(email, password):
try:
	cursor = g.db.execute("UPDATE users SET password = ? WHERE email=? ", [password, email])
	g.db.commit()
	return True
except:
	return False



def insert_token(token, email):
	try:
		cursor = g.db.execute("INSERT INTO tokenlist VALUES(?,?)" , [token, email])
		g.db.commit()
		return True
	except:
		return False

def find_inlogged(token):
	cursor = g.db.execute("SELECT email FROM tokenlist WHERE token = ?", [token])
	email = cursor.fetchall()
	cursor.close()
	return email

def remove_token(token):
	cursor = g.db.execute("DELETE FROM tokenlist WHERE token = ?", [token])
	g.db.commit()

def get_messages(email)
	cursor = g.db.execute("SELECT * from messages where receiver="email")
	messages = cursor.fetchall();
	cursor.close()
