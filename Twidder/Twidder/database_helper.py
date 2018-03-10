from flask import Flask
import sqlite3
from flask import g
import json

DATABASE = './Twidder/database.db'
#/home/malbr878/TDDD97/backend/database.db



#connect to database
def connect_db():
	print("Connected")
	g.db = sqlite3.connect(DATABASE)
	#g.db.execute("PRAGMA foreign_keys=1;")




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
		cursor = g.db.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?)",[email, firstname, familyname, password, sex, city, country])
		g.db.commit()

		return True
	except sqlite3.OperationalError, msg:
		print(msg)
		return False



#find a user from the database
def find_user(email):
	result = []
	cursor = g.db.execute("SELECT * FROM users WHERE email = ?", [email])
	#commit
	rows = cursor.fetchall()
	cursor.close()
	for index in range(len(rows)):
		result.append({'email':rows[index][0], 'firstname':rows[index][1],
			'familyname':rows[index][2], 'password':rows[index][3],
			'sex':rows[index][4], 'city':rows[index][5],
			'country':rows[index][6]})
	return (result[0] if result else None)




def remove_user(email):
	#connect = connect_db()

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



def check_password(email):
	cursor = g.db.execute("SELECT password FROM users WHERE email = ?", [email])
	passwrd = cursor.fetchall()
	cursor.close()
	return (passwrd[0] if passwrd else None)

def update_password(email, password):
	try:
		cursor = g.db.execute("UPDATE users SET password = ? WHERE email=?", [password, email])
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
	result = cursor.fetchall()
	cursor.close()
	return (result[0][0] if result else None)

def find_token(email):
	cursor = g.db.execute("SELECT token FROM tokenlist WHERE email = ?", [email])
	result = cursor.fetchall()
	cursor.close()
	return (result if result else None)

def remove_token(token):
	cursor = g.db.execute("DELETE FROM tokenlist WHERE token = ?", [token])
	g.db.commit()


def get_messages(email):
	cursor = g.db.execute("SELECT message FROM messages WHERE receiver = ?", [email])
	result = cursor.fetchall()
	cursor.close()
	return (result if result else None)


#def delete_logged_in_by_email(email):
#	cursor = g.db.execute("DELETE FROM tokenlist WHERE email = ?", [email])
#	g.db.commit()
