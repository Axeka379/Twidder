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
def sign_in(email, password):

@app.route('/signup')
def sign_up():

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
