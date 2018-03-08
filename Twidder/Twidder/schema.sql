DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS tokenlist;

CREATE TABLE users (
	email text NOT NULL PRIMARY KEY,
	firstname text NOT NULL,
	familyname text NOT NULL,
	password text NOT NULL,
	sex text NOT NULL,
	city text NOT NULL,
	country text NOT NULL
);

CREATE TABLE messages (
	sender text NOT NULL,
	message text NOT NULL,
	receiver text NOT NULL,
	FOREIGN KEY (sender) REFERENCES users(email),
	FOREIGN KEY (receiver) REFERENCES users(email)
);

CREATE TABLE tokenlist (
	token text NOT NULL PRIMARY KEY,
	email text NOT NULL,
	FOREIGN KEY (email) REFERENCES users(email)
);
