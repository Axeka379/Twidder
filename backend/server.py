from flask import Flask, app, request
from random import randint
import database_helper
import json


app = Flask(__name__)
app.debug = True

@app.before_request
def before_request():
	database_helper.connect_db()

@app.teardown_request
def teardown_request(exception):
	database_helper.close_db()


@app.route('/login')
def sign_in():
	email = request.args.get('email')
	password = request.args.get('password')

	if find_user(email) is not None && find_user(email)['password'] == password:

		letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        token = "";
        for i in range(0, 35):
          token += letters[randint(0, 35)]
		  insert_token(token, email)

		return json.dumps({"Success": True, "message": "Successfully signed in", "data": token})

	else:
		return json.dumps({"Success": False, "message": "Wrong username or password"})



@app.route('/signup')
def sign_up():

	if find_user(request.args.get('email')) is not None:

		user = {
			'email' : request.args.get('email')
			'password' : request.args.get('password')
			'firstname' : request.args.get('firstname')
			'familyname' : request.args.get('familyname')
			'sex' : request.args.get('sex')
			'city' : request.args.get('city')
			'country' : request.args.get('country')
		}

		if (insert_user(user['email'], user['firstname'], user['familyname'], user['sex'], user['city'] user['country'])):
			return json.dumps({"Success" : True, "Message": "Successfully signed up"})
		else:
			return json.dumps({"Success" : False, "Message": "Something went wrong"})
		else:
			return json.dumps({"Success" : False, "Message": "User already exists"})

@app.route('/signout')
def sign_out():
	token = request.args.get('token')
	if find_inlogged(token) is not None:
		remove_token(token)
		#not sure if it's correct to do json.dumps
		return json.dumps({"success": True, "message": "Successfully signed out."})
	else:
		return json.dumps({"success": False, "message": "You are not signed in."})



@app.route('/changepass')
def Change_password(token, oldPassword, newPassword):

@app.route('/databytoken')
def get_user_data_by_token():
	token = request.args.get('token')
	email = find_inlogged(token)
	return data_by_email(token, email)

@app.route('/databyemail')
def get_user_data_by_email():
	token = request.args.get('token')
	email = request.args.get('email')
	return data_by_email(token, email)

def data_by_email(token, email):
	if find_inlogged(token) is not None:
		if user = find_user(email) is not None:
			#does this work?
			user['password'] = None
			return json.dumps({"success": True, "message": "User data retrieved.", "data": user})
		else:
			return json.dumps({"success": False, "message": "No such user."})
	else:
		return json.dumps({"success": False, "message": "You are not signed in."})

@app.route('/messagebytoken')
def get_user_messages_by_token():
	token = request.args.get('token')

@app.route('/messagebyemail')
def get_user_messages_by_email():
	token = request.args.get('token')
	email = request.args.get('email')

def message_by_email(token, email):
	#we are here!
	#need to make a function in database_helper to get all messages for user

@app.route('/postmessage')
def post_message():
	token = request.args.get('token')
	message = request.args.get('message')
	receiver = request.args.get('receiver')
	if sender = find_inlogged(token) is not None:
		if receiver is None:
			receiver = sender
		if recipient = find_user(receiver) is not None:
			create_post(sender, message, recipient)
			return json.dumps({"success": True, "message": "Message posted"})
		else:
			return json.dumps({"success": False, "message": "No such user."})
	else:
		return json.dumps({"success": False, "message": "You are not signed in."})




@app.route("/")
def hello():
	return "Hello World!"

if __name__ == "__main__":
	app.run()
