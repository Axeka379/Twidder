from flask import Flask, app, request
from random import randint
import database_helper
import uuid
import json


app = Flask(__name__)
app.debug = True

@app.before_request
def before_request():
	database_helper.connect_db()

@app.teardown_request
def teardown_request(exception):
	database_helper.close_connection_db()


@app.route('/login')
def sign_in():
	data = request.json
	email = data["email"]
	password = data["password"]

	if database_helper.find_user(email) is not None and database_helper.find_user(email)['password'] == password:
		token = str(uuid.uuid4())
		database_helper.insert_token(token, email)
		return json.dumps({"Success": True, "message": "Successfully signed in", "data":token})

	else:
		return json.dumps({"Success": False, "message": "Wrong username or password"})



@app.route('/signup', methods=['POST'])
def sign_up():

	if database_helper.find_user(request.args.get('email')) is not None:
		user = request.json

		if database_helper.insert_user(user["email"], user["firstname"], user["familyname"],user["password"],user["sex"],user["city"], user["country"]):
			return json.dumps({"Success" : True, "Message": "Successfully signed up"})
		else:
			return json.dumps({"Success" : False, "Message": "Something went wrong"})
	else:
		return json.dumps({"Success" : False, "Message": "User already exists"})

@app.route('/signout')
def sign_out():
	token = request.json["token"]
	if database_helper.find_inlogged(token) is not None:
		database_helper.remove_token(token)
		#not sure if it's correct to do json.dumps
		return json.dumps({"success": True, "message": "Successfully signed out."})
	else:
		return json.dumps({"success": False, "message": "You are not signed in."})



@app.route('/changepass')
def Change_password():
	data = request.json
	token = data["token"]
	oldPassword = data["oldPassword"]
	newPassword = data["newPassword"]
	if database_helper.find_inlogged(token) is not None:
		email = database_helper.find_inlogged(token)
		if oldPassword == database_helper.find_user(email):
			database_helper.update_password(email, newPassword)
			return json.dumps({"success": True, "message": "Password changed."})
		else:
			return json.dumps({"success": False, "message": "Wrong password."})
	else:
		return Json.dumps({"success": False, "message": "You are not logged in."})


@app.route('/databytoken')
def get_user_data_by_token():
	token = request.json["token"]
	email = database_helper.find_inlogged(token)
	return data_by_email(token, email)

@app.route('/databyemail')
def get_user_data_by_email():
	data = request.json
	token = data["token"]
	email = data["email"]
	return data_by_email(token, email)

def data_by_email(token, email):
	if database_helper.database_helper.find_inlogged(token) is not None:
		if database_helper.find_user(email) is not None:
			user = database_helper.find_user(email)
			#does this work?
			user['password'] = None
			return json.dumps({"success": True, "message": "User data retrieved.", "data": user})
		else:
			return json.dumps({"success": False, "message": "No such user."})
	else:
		return json.dumps({"success": False, "message": "You are not signed in."})

@app.route('/messagebytoken')
def get_user_messages_by_token():
	token = request.json["token"]
	email = find_inlogged(token)
	message_by_email(token, email)

@app.route('/messagebyemail')
def get_user_messages_by_email():
	data = request.json
	token = data["token"]
	email = data["email"]
	message_by_email(token, email)

def message_by_email(token, email):
	if database_helper.find_inlogged(token) is not None:
		if database_helper.find_user(email) is not None:
			messages = database_helper.get_messages(email)
			return json.dumps({"success": True, "message": "User messages retrieved", "data": messages})
		else:
			return json.dumps({"success": False, "message": "No such user"})
	else:
		return json.dumps({"success": False, "message": "You are not signed in"})


	#we are here!
	#need to make a function in database_helper to get all messages for user

@app.route('/postmessage')
def post_message():
	data = request.json
	token = data["token"]
	message = data["messages"]
	receiver = data["receiver"]
	if database_helper.find_inlogged(token) is not None:
		sender = database_helper.find_inlogged(token)
		if receiver is None:
			receiver = sender
		if database_helper.find_user(receiver) is not None:
			recipient = database_helper.find_user(receiver)
			database_helper.create_post(sender, message, recipient)
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
