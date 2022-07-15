import os
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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

@app.route("/database_test",  methods=["GET", "POST"])
def database_test():
    """ simple view used to send test values to mongodb """
    if request.method == "POST":
        # get the value from the form to print
        value = request.form.get("test")
        test_entry = {
            "value": value
        }
        mongo.db.test_entries.insert_one(test_entry)
        print(value)

    return render_template("database-test.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
