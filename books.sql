--create a book table
CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  isbn CHAR(10) UNIQUE NOT NULL,
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  year INTEGER NOT NULL
);
