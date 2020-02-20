--create a book table
CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  isbn CHAR(10) UNIQUE NOT NULL,
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  year INTEGER NOT NULL
);

CREATE TABLE logins (
  id SERIAL PRIMARY KEY,
  username VARCHAR UNIQUE NOT NULL,
  hashed_password TEXT NOT NULL
);
