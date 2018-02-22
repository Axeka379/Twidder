DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS messages;
CREATE TABLE users (
	email text NOT NULL PRIMARY KEY,
	firstname text NOT NULL,
	familyname text NOT NULL,
	password text NOT NULL,
	sex INTEGER NOT NULL,	
	city text NOT NULL,
	country text NOT NULL,
	token text
);

CREATE TABLE messages (
	sender text NOT NULL,
	message text NOT NULL,
	receiver text NOT NULL,
	FOREIGN KEY (sender) REFERENCES users(email),
	FOREIGN KEY (receiver) REFERENCES users(email)
);

