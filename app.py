import os
from flask import (
    Flask, flash, render_template, 
    redirect, session, url_for, request)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    Recipe = list(mongo.db.Recipe.find())
    return render_template ("get_recipes.html", Recipe=Recipe)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already in use on mongoDB.
        existing_user = mongo.db.User.find_one(
            {"username": request.form.get("username").lower()})

        if (existing_user):
            flash ("Username already exists!")
            return redirect(url_for('register'))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }

        mongo.db.User.insert_one(register)

        # put user into new session cookie. 
        session["user"] = request.form.get("username").lower()
        flash("You are now registered. Enjoy!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        #check to see if user exists.
        existing_user = mongo.db.User.find_one(
            {"username": request.form.get("username").lower()}) 
        
        if existing_user:
            #check password is correct 
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))

            else:
                #incorrect password.
                flash("Password and/or username is incorrect!")
                return redirect(url_for("login"))

        else:
            #username doesnt exist.
            flash("Password and/or username is incorrect!")
            return redirect(url_for("login"))
            
    return render_template("login.html")

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    #grab session users username from DB
    username = mongo.db.User.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for('login'))

@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

