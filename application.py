import os, json

from flask import Flask, session, request, render_template, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Display Log In Form
@app.route("/")
@login_required
def index():
    #display form for Logging In
    return render_template("index.html")

#Allow user to get to the login page with GET method and process data with the POST method
@app.route("/login", methods=["GET", "POST"])
def login():
    #clear any session before logging in
    session.clear()

    ''' Log User In '''
    username = request.form.get("username")
    password = request.form.get("password")
    #user reached route via POST method(through the form)
    if request.method == "POST":

        #if username or password was NOT submitted
        if not username:
            return render_template("error.html", message="Please provide username")
        #if password was NOT submitted
        elif not password:
            return render_template("error.html", message="Please provide password")

        #find the username in the database
        rows = db.execute("SELECT * FROM logins WHERE username = :username", {"username":username})
        #get the username in the database
        result = rows.fetchone()

        #if no username or check_password_hash(hashed_password, password) is not valid
        if result == None or not check_password_hash(result[2], password):
            return render_template("error.html", message="Invalid username or password")

        '''If username and password matches'''
        # Use session to remember who has logged in
        session["id"] = result[0]
        session["username"] = result[1]
        return render_template("index.html")

    else:
        #return user to the login page
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    #clear the session
    session.clear()
    #redirect user to login page
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    ''' Register a User '''

    #Get information from the register form
    username = request.form.get("username")
    password = request.form.get("password")
    password_confirm = request.form.get("password_confirm")

    # If route via POST method
    if request.method == "POST":
        # Check if username already exist
        username_check = db.execute("SELECT * FROM logins WHERE username = :username", {"username": username}).fetchone()

        #if username exists display error
        if username_check:
            return render_template("error.html", message="username already exist")

        # check if password was submitted
        elif not password:
            return render_template("error.html", message="please enter a password")

        # Check if password the password_confirm was submitted
        elif not password_confirm:
            return render_template("error.html", message="please re-enter the password")

        # Check if password and password_confirm matches
        elif not password == password_confirm:
            return render_template("error.html", message="Passwords did not match!")

        # Hash the password
        hashedpassword = generate_password_hash(password)

        # Insert into the database
        db.execute("INSERT INTO logins (username, hashed_password) VALUES (:username, :hashedpassword)",
        {"username": username, "hashedpassword":hashedpassword})

        db.commit()

        #redirect user back to the login page
        return redirect("/login")

    # Re-route user to the register.html page
    else:
        return render_template("register.html")

@app.route("/search", methods=["POST"])
def search():
    ''' Allows user to search for books  '''
    if request.method == "POST":
        book_query = "%" + request.form.get("book") + "%"
        book_query = book_query.title()
        books = db.execute("SELECT * FROM books WHERE title LIKE :title OR author LIKE :author OR isbn LIKE :isbn", {"title": book_query, "author": book_query, "isbn": book_query})
        if books.rowcount == 0:
            return render_template("error.html", message="Sorry, we were unable to find any matching book")
        else:
            return render_template("result.html", books=books)
    else:
        return redirect("/")

@app.route("/book/<isbn>", methods=["GET", "POST"])
def book(isbn):
    '''Display book details'''
    row = db.execute("SELECT * FROM books where isbn = :isbn", {"isbn":isbn})
    book_details = row.fetchall()
    return render_template("book.html", book_details=book_details)
