import os
from flask import (Flask, render_template, url_for,
                   request, flash, session, redirect)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'emoji_hackathon_database'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def main():
    """ the main view of the app """
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register route to register users """
    if request.method == "POST":
        # check if the username already exist
        existing_user = mongo.db.test_entries.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists!")
            return redirect(url_for("register"))

        new_user = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.test_entries.insert_one(new_user)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("main", username=session["user"]))

    return render_template("register.html")


@app.route("/database_test",  methods=["GET", "POST"])
def database_test():
    """ simple view used to send test values to mongodb """

    all_entries = list(mongo.db.test_entries.find())

    if request.method == "POST":
        # get the value from the form to print
        value = request.form.get("test")
        test_entry = {
            "value": value
        }
        mongo.db.test_entries.insert_one(test_entry)
        print(value)
    return render_template("database-test.html", all_entries=all_entries)


@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        # check if the user exists
        existing_user = mongo.db.test_entries.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches what the user provided
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("main", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect username and/or password")
                return redirect(url_for("login"))

        else:
            # username does not exist
            flash("Incorrect username and/or password")
            return redirect(url_for("login"))

    return render_template("login.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
