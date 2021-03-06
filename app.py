from logging.handlers import RotatingFileHandler
import os
from pickle import OBJ
from flask import (Flask, render_template, url_for,
                   request, flash, session, redirect, jsonify)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import random
if os.path.exists("env.py"):
    import env
import json



app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'emoji_hackathon_database'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def main():
    """ the main view of the app """
    riddles = list(mongo.db.riddles.find())
    random_riddles = random.sample(riddles, 3)
    solve = random.choice(riddles)

    return render_template("index.html", riddles=random_riddles, solve=solve)


@app.route("/create", methods=["GET", "POST"])
def create():
    """ view to allow users to create riddles """
    if request.method == "POST":
        emoji_one = request.form.get("emoji-1") + " "
        emoji_two = request.form.get("emoji-2")
        if emoji_two == None:
            emoji_two = ""
        else:
            emoji_two = emoji_two + " "
        emoji_three = request.form.get("emoji-3")
        if emoji_three == None:
            emoji_three = ""
        else:
            emoji_three = emoji_three + " "
        emoji_four = request.form.get("emoji-4")
        if emoji_four == None:
            emoji_four = ""
        else:
            emoji_four = emoji_four + " "
        emoji_five = request.form.get("emoji-5")
        if emoji_five == None:
            emoji_five = ""
        else:
            emoji_five = emoji_five + " "
        emojis = emoji_one + emoji_two + emoji_three + emoji_four + emoji_five
        phrase = request.form.get("phrase")
        riddle = {
            "emojis": emojis,
            "phrase": phrase,
            "user": session["user"]
        }
        flash("Emoji Riddle submitted successfully")
        mongo.db.riddles.insert_one(riddle)
    return render_template("create.html")


@app.route("/edit_riddle/<e_id>", methods=["GET", "POST"])
def edit_riddle(e_id):
    """ view to allow users to edit riddles """
    riddle = mongo.db.riddles.find_one({"_id": ObjectId(e_id)})
    if request.method == "POST":
        emoji_one = request.form.get("emoji-1") + " "
        emoji_two = request.form.get("emoji-2")
        if emoji_two == None:
            emoji_two = ""
        else:
            emoji_two = emoji_two + " "
        emoji_three = request.form.get("emoji-3")
        if emoji_three == None:
            emoji_three = ""
        else:
            emoji_three = emoji_three + " "
        emoji_four = request.form.get("emoji-4")
        if emoji_four == None:
            emoji_four = ""
        else:
            emoji_four = emoji_four + " "
        emoji_five = request.form.get("emoji-5")
        if emoji_five == None:
            emoji_five = ""
        else:
            emoji_five = emoji_five + " "
        emojis = emoji_one + emoji_two + emoji_three + emoji_four + emoji_five
        phrase = request.form.get("phrase")
        riddle = {
            "emojis": emojis.strip(),
            "phrase": phrase,
            "user": session["user"]
        }
        mongo.db.riddles.replace_one({"_id": ObjectId(e_id)}, riddle)
        flash("Emoji Riddle updated successfully")
        return redirect(url_for("profile", username=session["user"]))
    emojis = riddle["emojis"].split()
    return render_template("edit_riddle.html", emojis=emojis, riddle=riddle)


@app.route("/play/<id>", methods=["GET", "POST"])
def play(id):
    next_riddle=None
    try:
        next_riddle = mongo.db.riddles.find({"_id": {"$gt": ObjectId(id) }}).limit(1)
        next_riddle = next_riddle.next()
    except:
        next_riddle = mongo.db.riddles.find_one()
    print('next', next_riddle)
    entry = mongo.db.riddles.find_one(
        {"_id": ObjectId(id)})
    riddle = entry["emojis"]
    answer = entry["phrase"]
    previous_rating = None
    number_of_ratings = 0
    if "rating" in entry:
        previous_rating=entry["rating"]
    if "number_of_ratings" in entry:
        number_of_ratings = entry["number_of_ratings"]
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if (is_ajax):
        if request.method == 'POST':
            user = session["user"]
            previous_rating_for_operation = None
            if previous_rating: 
                previous_rating_for_operation = previous_rating
            else: 
                previous_rating_for_operation = 0
            rating = float(request.data.decode())
            new_rating = (float(previous_rating_for_operation) * number_of_ratings) + rating
            print(new_rating)
            new_rating = new_rating / (number_of_ratings + 1)
            print(previous_rating, "previous_rating")
            print(rating, "rating")
            print(new_rating, "new_rating")
            mongo.db.riddles.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": {"rating": new_rating, 
            "number_of_ratings": number_of_ratings + 1,
            "last_rated_by": user,
            "last_rating_received": rating,
            }})
            return {"message": "Thanks for Rating!", "rating": new_rating}
        elif request.method == 'GET':
            return {"answer": answer}
    initial_rating_for_template = None
    if previous_rating:
        initial_rating_for_template = previous_rating
        initial_rating_for_template = round(initial_rating_for_template, 2)
    else: 
        initial_rating_for_template = "No rating yet"
    return render_template("play.html", next_riddle=next_riddle, riddle=riddle, answer=answer, rating=initial_rating_for_template)


@app.route("/playground")
def playground():
    """ View to show all the riddles on database for users to guess"""
    # check if user is logged in
    if session.get('user'):
        riddles = list(mongo.db.riddles.find())
        return render_template("playground.html", riddles=riddles)
    flash("You have to login first")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register route to register users """
    if request.method == "POST":
        # check if the username already exist
        existing_user = mongo.db.users.find_one(
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

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login users view """
    if request.method == "POST":
        # check if the user exists
        existing_user = mongo.db.users.find_one(
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


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """ view current logged in user profile to edit or delete riddles"""
    # grab the session's user username from db
    user = mongo.db.users.find_one(
        {"username": username})
    # get riddles by the logged in user
    riddles = None
    try:
        riddles = list(mongo.db.riddles.find({"user": username}))
    except:
        riddles = "none"
    print(riddles, "riddles")
    if session["user"]:
        return render_template("profile.html", username=username, riddles=riddles)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """ log out current logged in user"""
    # remove user from session cookie
    flash("You have been logged out successfully!")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/delete_riddle/<username>/<r_id>")
def delete_riddle(username, r_id):
    """ Delete riddle """
    username=username
    mongo.db.riddles.delete_one({"_id": ObjectId(r_id)})
    flash("Emoji Riddle deleted successfully")
    print(r_id)
    return redirect(url_for("profile", username=username))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
