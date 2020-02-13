import os

from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

#Sucess or Failure Log In
@app.route("/login", methods=["POST"])
def login():
    # Get information from user on the form
    username = request.form.get("username")
    password = request.form.get("password")

    # Make sure username and password exists
    if db.execute("SELECT * FROM logins WHERE username = :username AND password = :password", {"username":username, "password":password}).rowcount != 0:
        return render_template("success.html", username=username, message="You are currently logged in")
    else:
        return render_template("error.html", message="Invalid Username or Password")

#Register Form
@app.route("/register")
def register():
    # Display the register form
    return render_template("register.html")

#Sucess or Failure Form
@app.route("/registerSubmit", methods=["POST"])
def registerSubmit():
    #Get information from the register form
    username = request.form.get("username")
    password = request.form.get("password")

    # Check if username is already registered
    if db.execute("SELECT * FROM logins WHERE username = :username", {"username": username}).rowcount ==0:
        db.execute("INSERT INTO logins (username, password) VALUES (:username, :password)",
        {"username": username, "password":password})
        db.commit()
        return render_template("success.html", username=username, message="You have sucessfully registered. Please Log In")
    else:
        return render_template("error.html", message="Username has already been taken")
