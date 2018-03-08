
from flask import Flask, app, request
from random import randint

import database_helper as dh

import uuid
import json


app = Flask(__name__)
app.debug = True

import runserver

@app.route('/')
@app.route('/client')
def client():
	#client.html or /static/client.html???
    return app.send_static_file('client.html')

@app.before_request
def before_request():
	database_helper.connect_db()

@app.teardown_request
def teardown_request(exception):
	database_helper.close_connection_db()


@app.route('/signin', methods=['POST'])
def sign_in():
    data = request.json
    email = data["email"]
    password = data["password"]
    print(password)
    print(email)

    #database_helper.delete_logged_in_by_email(email)

    if database_helper.find_user(email) is not None and database_helper.find_user(email)["password"] == password:
        print("after find user")
        token = str(uuid.uuid4())
        database_helper.insert_token(token, email)
        print("after insert token")
        return json.dumps({"Success": True, "message": "Successfully signed in", "data":token})

    else:
    	return json.dumps({"Success": False, "message": "Wrong username or password"})



@app.route('/signup', methods=['POST'])
def sign_up():
	user = request.json
	if user['email'] == "" or user['password'] == "" or user["sex"] == "" or user["firstname"] == "" or user["familyname"] == "" or user["city"] == "" or user["country"] == "" or len(user["password"]) < 6:
		return json.dumps({"Success" : False, "Message": "Bad input"})
	if database_helper.find_user(user['email']) is None:



		if database_helper.insert_user(user["email"], user["firstname"], user["familyname"],user["password"],user["sex"],user["city"], user["country"]):
			return json.dumps({"Success" : True, "Message": "Successfully signed up"})
		else:
			return json.dumps({"Success" : False, "Message": "Something went wrong"})
	else:
		return json.dumps({"Success" : False, "Message": "User already exists"})

@app.route('/signout', methods=['POST'])
def sign_out():
	token = request.json["token"]
	if database_helper.find_inlogged(token) is not None:
		database_helper.remove_token(token)
		#not sure if it's correct to do json.dumps
		return json.dumps({"Success": True, "message": "Successfully signed out."})
	else:
		return json.dumps({"Success": False, "message": "You are not signed in."})



@app.route('/changepass', methods=['POST'])
def Change_password():
    data = request.json
    token = data["token"]
    oldPassword = data["oldpassword"]
    newPassword = data["newpassword"]
    if database_helper.find_inlogged(token) is not None:
    	email = database_helper.find_inlogged(token)
    	if oldPassword == database_helper.find_user(email)["password"]:
    		database_helper.update_password(email, newPassword)
    		return json.dumps({"Success": True, "message": "Password changed."})
    	else:
	        return json.dumps({"Success": False, "message": "Wrong password."})
    else:
    	return Json.dumps({"Success": False, "message": "You are not logged in."})


@app.route('/databytoken', methods=['GET'])
def get_user_data_by_token():
	#token = request.json["token"]
	token = request.headers.get('token')
	email = database_helper.find_inlogged(token)
	return data_by_email(token, email)

@app.route('/databyemail', methods=['GET'])
def get_user_data_by_email():
    #data = request.json
    token = request.headers.get('token')
    email = request.headers.get('email')
    print(email)
    return data_by_email(token, email)

def data_by_email(token, email):
    if database_helper.find_inlogged(token) is not None:
    	if database_helper.find_user(email) is not None:
    		user = database_helper.find_user(email)

    		del user['password']
    		return json.dumps({"Success": True, "message": "User data retrieved.", "data": user})
    	else:
    		return json.dumps({"Success": False, "message": "No such user."})
    else:
    	return json.dumps({"Success": False, "message": "You are not signed in."})

@app.route('/messagebytoken', methods=['GET'])
def get_user_messages_by_token():
	token = request.headers.get('token')
	email = database_helper.find_inlogged(token)
	return message_by_email(token, email)

@app.route('/messagebyemail', methods=['GET'])
def get_user_messages_by_email():

	token = request.headers.get('token')
	email = request.headers.get('email')
	return message_by_email(token, email)

def message_by_email(token, email):
	if database_helper.find_inlogged(token) is not None:
		if database_helper.find_user(email) is not None:
			messages = database_helper.get_messages(email)
			if messages is not None:
				sum = ""
				for message in messages:
					#do we have to add the senders email?
					sum += message[0] + "\n"
				return json.dumps({"Success": True, "message": "User messages retrieved", "data": sum})
			return json.dumps({"Success": True, "message": "No messages on this users profile", "data": ""})
		else:
			return json.dumps({"Success": False, "message": "No such user"})
	else:
		return json.dumps({"Success": False, "message": "You are not signed in"})


	#we are here!
	#need to make a function in database_helper to get all messages for user

@app.route('/postmessage', methods=['POST'])
def post_message():
	data = request.json
	token = data["token"]
	message = data["messages"]
	receiver = data["receiver"]
	#print(receiver)
	if database_helper.find_inlogged(token) is not None:
		sender = database_helper.find_inlogged(token)
		if receiver is None:
			receiver = sender
		if database_helper.find_user(receiver) is not None:
			recipient = database_helper.find_user(receiver)['email']
			print(recipient)
			print(database_helper.create_post(sender, message, recipient))
			return json.dumps({"Success": True, "message": "Message posted"})
		else:
			return json.dumps({"Success": False, "message": "No such user."})
	else:
		return json.dumps({"Success": False, "message": "You are not signed in."})




@app.route("/")
def hello():
	return "Hello World!"

if __name__ == "__main__":
	app.run()
