from flask import Flask, app, request
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

	if(find_user(email) != NULL && check_password(password) == password)
	{
		var letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
        var token = "";
        for (var i = 0 ; i < 36 ; ++i)
		{
          token += letters[Math.floor(Math.random() * letters.length)];
        }

	return {"Success": True, "message": "Successfully signed in", "data": token};
	}
	else
	{
		return {"Success": False, "message": "Wrong username or password"};
	}


@app.route('/signup')
def sign_up():

	if(find_user(request.args.get('email'))	!= NULL) {

		var user = {
		'email' : request.args.get('email')
		'password' : request.args.get('password')
		'firstname' : request.args.get('firstname')
		'familyname' : request.args.get('familyname')
		'sex' : request.args.get('sex')
		'city' : request.args.get('city')
		'country' : request.args.get('country')
		}

		if (insert_user(user['email'], user['firstname'], user['familyname'], user['sex'], user['city'] user['country'], find_user(user['email'].data)))
		{
			return {"Success" : True, "Message": "Successfully signed up"}
		}
		else {
			return {"Success" : False, "Message": "Something went wrong"}
	}
	else{
		return {"Success" : False, "Message": "User already exists"}
		}
}

@app.route('/signout')
def sign_out(token):

@app.route('/changepass')
def Change_password(token, oldPassword, newPassword):

@app.route('/databytoken')
def get_user_data_by_token(token):


@app.route('/databyemail')
def get_user_data_by_email(token, email):

@app.route('/messagebytoken')
def get_user_messages_by_token(token):

@app.route('/messagebyemail')
def get_user_messages_by_email(token, email):

@app.route('/postmessage')
def post_message(token, content, toemail)



@app.route("/")
def hello():
	return "Hello World!"

if __name__ == "__main__":
	app.run()
