
from flask import Flask, app, request
from random import randint
from geventwebsocket import WebSocketError

import database_helper as dh

import hashlib, uuid
import json


app = Flask(__name__)
app.debug = True

import Twidder

sockets = {}


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
    hash = data["hash"]


    #hash_check2 = hashlib.sha512(hash).hexdigest()
    hash_check = hashlib.sha512(email+password).hexdigest()

    if(hash_check != hash):
    	return json.dumps({"Success": False, "message": "Invalid request"})


    #database_helper.delete_logged_in_by_email(email)
    result = database_helper.find_user(email)
    print(result)
    if result is not None: # and database_helper.find_user(email)["password"] == password:

        hashed_password = hashlib.sha512(password + database_helper.find_user(email)["salt"]).hexdigest()

        if hashed_password == database_helper.find_user(email)["password"]:
            print("after find user")
            token = str(uuid.uuid4())
            database_helper.insert_token(token, email)
            print("after insert token")
            return json.dumps({"Success": True, "message": "Successfully signed in", "data":token})
        else:
    	    return json.dumps({"Success": False, "message": "Wrong username or password"})

    else:
    	return json.dumps({"Success": False, "message": "Wrong username or password"})


@app.route('/reload', methods=['POST'])
def reload():
    data = request.json
    email = data["email"]
    print("################## ", email)

    #Socket. log out other people and update charts
    if email is not None:
        #if token not in sockets:
        #    sockets[token] = websocket
        #sockets[token] = websocket
        if database_helper.find_token(email)is not None:
            if email in sockets:
                print(email)
                sockets[email].send(json.dumps({"success": True, "updateloggedin":False}))
                sockets[email].close()
                del sockets[email]

        for othersock in sockets.items():
            male, female = calculateGender()
            if othersock[1] is not None:
                othersock[1].send(json.dumps({"success":True, "updateloggedin":True, "online":len(sockets)+1, "offline":(database_helper.amount_registered() - len(sockets)-1), "male":male,"female":female}))

        return json.dumps({"Success": True, "message": "Successfully sent data to sockets", "data":email})

    else:
    	return json.dumps({"Success": False, "message": "something went wrong"})



@app.route('/signup', methods=['POST'])
def sign_up():
    user = request.json
    if user['email'] == "" or user['password'] == "" or user["sex"] == "" or user["firstname"] == "" or user["familyname"] == "" or user["city"] == "" or user["country"] == "" or len(user["password"]) < 6:
    	return json.dumps({"Success" : False, "Message": "Bad input"})
    if database_helper.find_user(user['email']) is None:

        salt = uuid.uuid4().hex
        password_hash = hashlib.sha512(user["password"] + salt).hexdigest()
    	if database_helper.insert_user(user["email"], user["firstname"] ,user["familyname"] ,password_hash ,user["sex"],user["city"], user["country"], salt):

            for othersock in sockets.items():
                male, female = calculateGender()
                if othersock[1] is not None:
                    othersock[1].send(json.dumps({"success":True, "updateloggedin":True, "online":len(sockets), "offline":(database_helper.amount_registered() - (len(sockets))), "male":male,"female":female}))

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

		return json.dumps({"Success": True, "message": "Successfully signed out."})
	else:
		return json.dumps({"Success": False, "message": "You are not signed in."})



@app.route('/changepass', methods=['POST'])
def Change_password():
    data = request.json
    hash = data["hash"]
    oldPassword = data["oldpassword"]
    newPassword = data["newpassword"]
    email = data["email"]

    token = database_helper.find_inlogged_mail(email)

    hash_check = hashlib.sha512(oldPassword+newPassword+token[0]).hexdigest()

    if(hash_check != hash):
        return json.dumps({"Success": False, "message": "Invalid request"})



    newPasswordHashed = hashlib.sha512(newPassword + database_helper.find_user(email)["salt"]).hexdigest()

    oldPasswordHashed = hashlib.sha512(oldPassword + database_helper.find_user(email)["salt"]).hexdigest()
    if database_helper.find_inlogged_mail(email) is not None:
    	if oldPasswordHashed == database_helper.find_user(email)["password"]:
    		database_helper.update_password(email, newPasswordHashed)
    		return json.dumps({"Success": True, "message": "Password changed."})
    	else:
	        return json.dumps({"Success": False, "message": "Wrong password."})
    else:
    	return Json.dumps({"Success": False, "message": "You are not logged in."})


def create_hash(password, salt):
    return hashlib.sha512(password + salt).hexdigest()


def check_hash(hash, params, token):
    return hashlib.sha512(params + token).hexdigest() == hash

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



@app.route('/socket')
def api():
    websocket = request.environ['wsgi.websocket']
    if websocket is None:
        print("there is no socket")
        return json.dumps({"success": False, "messages":"Didn't get a socket"})

    token = ""
    email = ""
    otherToken = ""
    try:

        data = json.loads(websocket.receive())
        email = data["email"]
        '''
        email = database_helper.find_inlogged(token)

        if email is not None:
            if token not in sockets:
                sockets[token] = websocket



            for tok in database_helper.find_token(email):
                otherToken = tok[0]
                print(otherToken)
                if otherToken != token and otherToken is not None:
                    sockets[otherToken].send(json.dumps({"success": True, "updateloggedin":False}))
                    sockets[otherToken].close()
                    del sockets[otherToken]

            for othersock in sockets.items():
                male, female = calculateGender()
                if othersock[1] is not None:
                    othersock[1].send(json.dumps({"success":True, "updateloggedin":True, "online":len(sockets), "offline":(database_helper.amount_registered() - len(sockets)), "male":male,"female":female}))
        '''
        male, female = calculateGender()
        sockets[email] = websocket
        websocket.send(json.dumps({"success": True, "updateloggedin":True, "online":len(sockets), "offline":(database_helper.amount_registered() - len(sockets)), "male":male,"female":female, "male":male,"female":female}));

        #websocket.send(json.dumps({"success":True, "updateloggedin":True, "number":len(sockets)}))

        while True:
            data = websocket.receive()
            #websocket.send(json.dumps({"success":True, "updateloggedin":True, "number":len(sockets)}))
            if data is None:
                del sockets[email]
                male, female = calculateGender()
                for othersock in sockets.items():
                    if othersock[1] is not None:
                        othersock[1].send(json.dumps({"success":True, "updateloggedin":True, "online":len(sockets), "offline":(database_helper.amount_registered() - len(sockets)), "male":male,"female":female}))

                websocket.close();
                return json.dumps({"success": False, "messages":"connection closed"})


    except WebSocketError as e:
        print("error")
        del sockets[email]
        male, female = calculateGender()
        for othersock in sockets.items():
            if othersock[1] is not None:
                othersock[1].send(json.dumps({"success":True, "updateloggedin":True, "online":len(sockets), "offline":(database_helper.amount_registered() - len(sockets)), "male":male,"female":female}))

        json.dumps({"success": False, "messages":"something went wrong"})










'''@app.route('/regsocket')
def regapi():
    websocket = request.environ['wsgi.websocket']
    if websocket is None:
        print("there is no socket")
        return json.dumps({"success": False, "messages":"Didn't get a socket"})

    try:
        print("sent");
        data = json.loads(websocket.receive())
        if(data["success"]):
            male, female = calculateGender()
            for othersock in sockets.items():
                if othersock[1] is not None:
                    othersock[1].send(json.dumps({"success":True, "updateloggedin":True, "online":len(sockets), "offline":(database_helper.amount_registered() - len(sockets)), "male":male,"female":female}))

        websocket.close();


    except WebSocketError as e:
        print("error")
        json.dumps({"success": False, "messages":"something went wrong"})
'''


def calculateGender():
    data = database_helper.amount_of_different_genders()
    male = 0
    female = 0
    for x in data:
        print(x[0])
        if(x[0] == "male"):
            male += 1
        else:
            female += 1

    return male, female

def check_hash(hash, params, token):
    return hashlib.sha512(params + token).hexdigest() == hash


#@app.route("/")
#def hello():
#	return "Hello World!"

#if __name__ == "__main__":
#	app.run()
