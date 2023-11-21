import os
import sys

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta

from helpers import error, login_required, flight_lookup
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# APIs
flight_api = os.getenv('AIRLABS_DATA_API_KEY')
weather_api = os.getenv('OPENWEATHER_API_KEY')

# Configure database
con = sqlite3.connect("flights.db", check_same_thread=False)
db = con.cursor()

# Make temporary flight list
userList = []

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Follow Flights"""
    # Update flight list to user's list
    if len(userList) == 0:
        userflights = db.execute("SELECT * FROM flightlist WHERE user_id = ?", (session["user_id"], ))
        flights = userflights.fetchall()
        for f in flights:
            flight_result = flight_lookup(flight_api, weather_api, f[2])
            # Flight search error
            if "message" in flight_result:
                db.execute("DELETE FROM flightlist WHERE flight_number = ?", (f[2], ))
                con.commit()

            # Flight found
            else:
                #add result to list
                userList.append(flight_result)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST" and "flightSearch" in request.form:

        # Ensure symbol was submitted
        if not request.form.get("flightSearch"):
            return error("Please enter a flight number.")

        # Ensure user only has maximum of 5 flights
        rows = db.execute("SELECT * FROM flightlist WHERE user_id = ?", (session["user_id"], ))
        if len(rows.fetchall()) == 5:
            return error("Maximum of five flights reached.")

        # Remove all spaces from input
        search = request.form.get("flightSearch").replace(" ", "")

        # Use lookup function
        flight_result = flight_lookup(flight_api, weather_api, search)

        # Flight search error
        if "message" in flight_result:
            return error(flight_result['message']+".")

        # Flight found
        else:
            data = (
                {"user_id": session["user_id"], "flight_number": flight_result['flight_number']}
            )

            # Ensure flight not in list
            rows = db.execute("SELECT * FROM flightlist WHERE user_id = (:user_id) AND flight_number = (:flight_number)", data)
            if len(rows.fetchall()) == 1:
                return error("Flight is already added.")

            # Record new followed flight
            db.execute("INSERT INTO flightlist (user_id, flight_number) VALUES (:user_id, :flight_number);", data)
            con.commit()

            #add result to list
            userList.append(flight_result)

            return redirect("/")

    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST" and "flightRemove" in request.form:
        # Remove selected flight
        data = (
            {"user_id": session["user_id"], "flight_number": request.form.get("flightRemove")}
        )
        db.execute("DELETE FROM flightlist WHERE user_id = (:user_id) AND flight_number = (:flight_number);", data)
        con.commit()

        # Update userList
        userList.clear()
        userflights = db.execute("SELECT * FROM flightlist WHERE user_id = ?", (session["user_id"], ))
        flights = userflights.fetchall()
        for f in flights:
            flight_result = flight_lookup(flight_api, weather_api, f[2])
            # Flight search error
            if "message" in flight_result:
                db.execute("DELETE FROM flightlist WHERE flight_number = ?", (f[2], ))
                con.commit()

            # Flight found
            else:
                #add result to list
                userList.append(flight_result)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html", userList = userList)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("Please provide a username.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("Please provide a password.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"), ))
        if len(rows.fetchall()) != 1:
            return error("Username invalid.")

        # Ensure password is correct
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"), ))
        hash_password = rows.fetchall()[0][2]
        if not check_password_hash(hash_password, request.form.get("password")):
            return error("Wrong password.")

        # Remember which user has logged in
        data = (
            {"username": request.form.get("username"), "hash": hash_password}
        )
        user_id = db.execute("SELECT id FROM users WHERE username = (:username) AND hash = (:hash)", data)
        session["user_id"] = user_id.fetchone()[0]

        # Update flight list to user's list
        userflights = db.execute("SELECT * FROM flightlist WHERE user_id = ?", (session["user_id"], ))
        flights = userflights.fetchall()
        for f in flights:
            flight_result = flight_lookup(flight_api, weather_api, f[2])
            # Flight search error
            if "message" in flight_result:
                db.execute("DELETE FROM flightlist WHERE flight_number = ?", (f[2], ))
                con.commit()

            # Flight found
            else:
                #add result to list
                userList.append(flight_result)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Clear userList
    userList.clear()

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("Please provide a username.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("Please provide a password.")

        # Ensure password and confirmation are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return error("Please provide matching passwords.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"), ))

        # Ensure username is new
        if len(rows.fetchall()) == 1:
            return error("Username already exists.")

        # Hash password
        hash_password = generate_password_hash(request.form.get("password"))

        # Insert new user into database
        data = (
            {"username": request.form.get("username"), "hash": hash_password}
        )
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash);", data)
        con.commit()

        # Automatically log new user in
        user_id = db.execute("SELECT id FROM users WHERE username = (:username) AND hash = (:hash)", data)
        session["user_id"] = user_id.fetchone()[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")