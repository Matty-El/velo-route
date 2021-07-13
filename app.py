import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
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
@app.route("/get_routes")
def get_routes():
    routes = mongo.db.routes.find()
    return render_template("routes.html", routes=routes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            # remember to add password confirmation
            # remember to add user type
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # add the new user into session cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check is the username exists in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # check that hashed password is the password entered by user
            if check_password_hash(
                        existing_user["password"],
                        request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # passwords do not match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            # username does not exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # get session user's username from the database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    first_name = mongo.db.users.find_one(
        {"username": session["user"]})["first_name"]
    last_name = mongo.db.users.find_one(
        {"username": session["user"]})["last_name"]
    email = mongo.db.users.find_one(
        {"username": session["user"]})["email"]

    if session["user"]:
        return render_template("profile.html", username=username,
                               first_name=first_name, last_name=last_name,
                               email=email)

    return redirect(url_for("login"))


@app.route("/add_route", methods=["GET", "POST"])
def add_route():
    if request.method == "POST":
        route = {
            "category_name": request.form.get("category_name"),
            "route_name": request.form.get("route_name"),
            "route_image": request.form.get("route_image"),
            "route_distance": request.form.get("route_distance"),
            "route_difficulty": request.form.get("route_difficulty"),
            "route_description": request.form.get("route_description"),
            "route_link": request.form.get("route_link"),
            "created_by": session["user"]
        }

        mongo.db.routes.insert_one(route)
        flash("Route Successfully Added")
        return redirect(url_for("get_routes"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    difficulty_levels = mongo.db.difficulty_levels.find().sort(
        "route_difficulty", 1)
    return render_template("add_route.html", categories=categories,
                           difficulty_levels=difficulty_levels)


@app.route("/edit_route/<route_id>", methods=["GET", "POST"])
def edit_route(route_id):

    if request.method == "POST":
        edit = {
            "category_name": request.form.get("category_name"),
            "route_name": request.form.get("route_name"),
            "route_image": request.form.get("route_image"),
            "route_distance": request.form.get("route_distance"),
            "route_difficulty": request.form.get("route_difficulty"),
            "route_description": request.form.get("route_description"),
            "route_link": request.form.get("route_link"),
            "created_by": session["user"]
        }

        mongo.db.routes.update({"_id": ObjectId(route_id)}, edit)
        flash("Route Successfully Edited")

    route = mongo.db.routes.find_one({"_id": ObjectId(route_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    difficulty_levels = mongo.db.difficulty_levels.find().sort(
        "route_difficulty", 1)
    return render_template("edit_route.html", route=route,
                           categories=categories,
                           difficulty_levels=difficulty_levels)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
