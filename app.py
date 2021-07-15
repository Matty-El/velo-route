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


@app.route("/route_search", methods=["GET", "POST"])
def route_search():
    route_query = request.form.get("route_query")
    routes = mongo.db.routes.find({"$text": {"$search": route_query}})
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


@app.route("/delete_route/<route_id>")
def delete_route(route_id):
    mongo.db.routes.remove({"_id": ObjectId(route_id)})
    flash("Route Deleted")
    return redirect(url_for("get_routes"))


@app.route("/get_cycling_tips")
def get_cycling_tips():
    cycling_tips = list(mongo.db.cycling_tips.find().sort(
                        "cycling_tip_name", 1))
    return render_template("cycling_tips.html", cycling_tips=cycling_tips)


@app.route("/add_cycling_tip", methods=["GET", "POST"])
def add_cycling_tip():
    if request.method == "POST":
        cycling_tip = {
            "category_name": request.form.get("category_name"),
            "cycling_tip_name": request.form.get("cycling_tip_name"),
            "cycling_tip_description": request.form.get(
                "cycling_tip_description"),
            "cycling_tip_image": request.form.get("cycling_tip_image"),
            "cycling_tip_link": request.form.get("cycling_tip_link"),
            "created_by": session["user"]
        }
        mongo.db.cycling_tips.insert_one(cycling_tip)
        flash("New Cycling Tip Added")
        return redirect(url_for("get_cycling_tips"))

    cycling_tip_categories = mongo.db.cycling_tip_categories.find().sort(
        "category_name", 1)
    return render_template("add_cycling_tip.html",
                           cycling_tip_categories=cycling_tip_categories)


@app.route("/edit_cycling_tip/<cycling_tip_id>", methods=["GET", "POST"])
def edit_cycling_tip(cycling_tip_id):
    if request.method == "POST":
        submit_cycling_tip = {
            "cycling_tip_name": request.form.get("cycling_tip_name"),
            "cycling_tip_description": request.form.get(
                "cycling_tip_description"),
            "cycling_tip_image": request.form.get("cycling_tip_image"),
            "cycling_tip_link": request.form.get("cycling_tip_link"),
            "created_by": session["user"]
        }
        mongo.db.cycling_tips.update(
            {"_id": ObjectId(cycling_tip_id)}, submit_cycling_tip)
        flash("Cycling Tip Updated")
        return redirect(url_for("get_cycling_tips"))

    cycling_tip = mongo.db.cycling_tips.find_one(
        {"_id": ObjectId(cycling_tip_id)})
    cycling_tip_categories = mongo.db.cycling_tip_categories.find().sort(
        "category_name", 1)
    return render_template("edit_cycling_tip.html", cycling_tip=cycling_tip,
                           cycling_tip_categories=cycling_tip_categories)


@app.route("/delete_cycling_tip/<cycling_tip_id>")
def delete_cycling_tip(cycling_tip_id):
    mongo.db.cycling_tips.remove({"_id": ObjectId(cycling_tip_id)})
    flash("Cycling Tip Deleted")
    return redirect(url_for("get_cycling_tips"))


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.insert_one(category)
        flash("New Category Added")
        return redirect(url_for("get_categories"))

    return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Category Updated")
        return redirect(url_for("get_categories"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Category Deleted")
    return redirect(url_for("get_categories"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
