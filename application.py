import os

from flask import Flask, session, request, render_template, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

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
def index():
    #display form for Logging In
    return render_template("index.html")

#Process data from Login Form accepting POST method
@app.route("/login", methods=["POST"])
def login():
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
        result = rows.fetchone()

        #check_password_hash(hashed_password, password)
        if result == None or not check_password_hash(result[2], password):
            return render_template("error.html", message="Invalid username or password")

        '''If username and password matches'''
        # Use session to remember who has logged in
        session["id"] = result[0]
        session["username"] = result[1]
        return render_template("success.html", message="You have sucessfully logged in")

    else:
        #return user to the login page
        return render_template("index.html")


    # Make sure username AND password exists
    if db.execute("SELECT * FROM logins WHERE username = :username AND password = :password", {"username":username, "password":password}).rowcount != 0:
        #display book review page
        return render_template("success.html", username=username, message="You are currently logged in")
    else:
        return render_template("error.html", message="Invalid Username or Password")

@app.route("/logout")
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

        return render_template("success.html", username=username, message="You have sucessfully registered. Please Log In")

    # Re-route user to the register.html page
    else:
        return render_template("register.html")
