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

# ------------------------ configuration ----------------------------------- #
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# ------------------------ home page --------------------------------------- #
@app.route("/")
def index():
    # first six routes for medium and large devices
    med_large_routes = mongo.db.routes.find().sort("_id", -1).limit(6)
    # first four routes for mobile devices
    small_routes = mongo.db.routes.find().sort("_id", -1).limit(3)
    return render_template(
        "index.html", med_large_routes=med_large_routes,
        small_routes=small_routes)


# ------------------------ users ------------------------------------------- #
@app.route("/join_us", methods=["GET", "POST"])
def join_us():
    # check if user is logged in
    if session.get("user"):
        # redirect to profile
        return redirect(url_for("profile", username=session["user"]))
    else:
        if request.method == "POST":
            # check if username exists in database
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})

            if existing_user:
                flash("Username already exists. Please log in.")
                return redirect(url_for("login"))

            join_us = {
                "username": request.form.get("username").lower(),
                "first_name": request.form.get("first_name"),
                "last_name": request.form.get("last_name"),
                "email": request.form.get("email"),
                "password": generate_password_hash(
                    request.form.get("password"))
            }
            mongo.db.users.insert_one(join_us)

            # add the new user into session cookie
            session["user"] = request.form.get("username").lower()
            flash("Welcome to VeloRoute")
            return redirect(url_for("profile", username=session["user"]))

        return render_template("join_us.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # check if user is logged in
    if session.get("user"):
        # redirect to profile
        return redirect(url_for("profile", username=session["user"]))
    else:
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
                    flash("Welcome back, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
                else:
                    # passwords do not match
                    flash("Incorrect Username or Password")
                    return redirect(url_for("login"))
            else:
                # username does not exist
                flash("Incorrect Username or Password")
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

    # only users can access the profile page
    if not session.get("user"):
        flash("Please join VeloRoute for full user access.")
        return render_template("403.html")

    # get session user's username and other details from the database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    first_name = mongo.db.users.find_one(
        {"username": session["user"]})["first_name"]
    last_name = mongo.db.users.find_one(
        {"username": session["user"]})["last_name"]
    email = mongo.db.users.find_one(
        {"username": session["user"]})["email"]
    routes = mongo.db.routes.find().sort("_id", -1)

    if session["user"]:
        # admin can view / edit all routes
        if session["user"] == "admin":
            routes = list(mongo.db.routes.find().sort("_id", -1))
        else:
            # user can view / edit own routes
            routes = list(
                mongo.db.routes.find({"created_by": session["user"]}).sort(
                    "_id", -1))

        return render_template("profile.html", username=username,
                               first_name=first_name, last_name=last_name,
                               email=email, routes=routes)

    return redirect(url_for("login"))


# ------------------------ cycling routes ---------------------------------- #
@app.route("/get_routes")
def get_routes():
    routes = mongo.db.routes.find().sort("_id", -1)
    return render_template("routes.html", routes=routes)


@app.route("/route_search", methods=["GET", "POST"])
def route_search():
    route_query = request.form.get("route_query")
    routes = mongo.db.routes.find({"$text": {"$search": route_query}})
    return render_template("routes.html", routes=routes)


@app.route("/add_route", methods=["GET", "POST"])
def add_route():

    # only users can access the add route page
    if not session.get("user"):
        flash("Please join VeloRoute for full user access.")
        return render_template("403.html")

    if request.method == "POST":
        route = {
            "category_name": request.form.get("category_name"),
            "route_name": request.form.get("route_name"),
            "route_image": request.form.get("route_image"),
            "route_distance": request.form.get("route_distance"),
            "route_difficulty": request.form.get("route_difficulty"),
            "country_name": request.form.get("country_name"),
            "route_description": request.form.get("route_description"),
            "route_link": request.form.get("route_link"),
            "created_by": session["user"]
        }

        mongo.db.routes.insert_one(route)
        flash("Route Successfully Added")
        return redirect(url_for("profile", username=session['user']))

    categories = mongo.db.categories.find().sort("category_name", 1)
    difficulty_levels = mongo.db.difficulty_levels.find().sort(
        "route_difficulty", 1)
    countries = mongo.db.countries.find().sort("country_name", 1)
    return render_template("add_route.html", categories=categories,
                           difficulty_levels=difficulty_levels,
                           countries=countries)


@app.route("/edit_route/<route_id>", methods=["GET", "POST"])
def edit_route(route_id):

    # only users can access the edit route page
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")

    if request.method == "POST":
        edit = {
            "category_name": request.form.get("category_name"),
            "route_name": request.form.get("route_name"),
            "route_image": request.form.get("route_image"),
            "route_distance": request.form.get("route_distance"),
            "route_difficulty": request.form.get("route_difficulty"),
            "country_name": request.form.get("country_name"),
            "route_description": request.form.get("route_description"),
            "route_link": request.form.get("route_link"),
            "created_by": session["user"]
        }

        mongo.db.routes.update({"_id": ObjectId(route_id)}, edit)
        flash("Route Successfully Edited")
        return redirect(url_for("profile", username=session['user']))

    route = mongo.db.routes.find_one({"_id": ObjectId(route_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    difficulty_levels = mongo.db.difficulty_levels.find().sort(
        "route_difficulty", 1)
    countries = mongo.db.countries.find().sort("country_name", 1)
    return render_template("edit_route.html", route=route,
                           categories=categories,
                           difficulty_levels=difficulty_levels,
                           countries=countries)


@app.route("/delete_route/<route_id>")
def delete_route(route_id):

    # only users can delete a route
    if not session.get("user"):
        flash("Please join us for full user access.")
        return render_template("403.html")

    mongo.db.routes.delete_one({"_id": ObjectId(route_id)})
    flash("Route Successfully Deleted")
    return redirect(url_for("profile", username=session['user']))


# ------------------------ cycling tips ------------------------------------ #
@app.route("/get_cycling_tips")
def get_cycling_tips():
    cycling_tips = list(mongo.db.cycling_tips.find().sort(
                        "_id", -1))
    return render_template("cycling_tips.html", cycling_tips=cycling_tips)


@app.route("/add_cycling_tip", methods=["GET", "POST"])
def add_cycling_tip():
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # admin only access
        if session["user"] == "admin":
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

            cycling_tip_categories = mongo.db.cycling_tip_categories.find(
            ).sort("category_name", 1)
            return render_template(
                "add_cycling_tip.html",
                cycling_tip_categories=cycling_tip_categories)
        else:
            # display 403 error page
            flash("You have tried to access an admin only page.")
            return render_template("403.html")


@app.route("/edit_cycling_tip/<cycling_tip_id>", methods=["GET", "POST"])
def edit_cycling_tip(cycling_tip_id):
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # admin only access
        if session["user"] == "admin":
            if request.method == "POST":
                submit_cycling_tip = {
                    "category_name": request.form.get("category_name"),
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
            cycling_tip_categories = mongo.db.cycling_tip_categories.find(
            ).sort("category_name", 1)
            return render_template(
                "edit_cycling_tip.html", cycling_tip=cycling_tip,
                cycling_tip_categories=cycling_tip_categories)
        else:
            # display 403 error page
            flash("You have tried to access an admin only page.")
            return render_template("403.html")


@app.route("/delete_cycling_tip/<cycling_tip_id>")
def delete_cycling_tip(cycling_tip_id):
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # admin only access
        if session["user"] == "admin":
            mongo.db.cycling_tips.delete_one({"_id": ObjectId(cycling_tip_id)})
            flash("Cycling Tip Deleted")
            return redirect(url_for("get_cycling_tips"))
        else:
            # display 403 error page
            flash("You have tried to access an admin only page.")
            return render_template("403.html")


# ------------------------ categories WARNING ITUSER ACCESS ONLY ----------- #
# get all categories
@app.route("/get_categories")
def get_categories():
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # ituser only access
        if session["user"] == "ituser":
            categories = list(mongo.db.categories.find(
            ).sort("category_name", 1))
            cycling_tip_categories = list(
                mongo.db.cycling_tip_categories.find(
                ).sort("category_name", 1))
            difficulty_levels = list(mongo.db.difficulty_levels.find().sort(
                                    "route_difficulty", 1))
            return render_template(
                "categories.html", categories=categories,
                cycling_tip_categories=cycling_tip_categories,
                difficulty_levels=difficulty_levels)
        else:
            # display 403 error page
            flash("You have tried to access an IT user only page.")
            return render_template("403.html")


# route categories
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # ituser only access
        if session["user"] == "ituser":
            if request.method == "POST":
                category = {
                    "category_name": request.form.get("category_name")
                }
                mongo.db.categories.insert_one(category)
                flash("New Route Category Added")
                return redirect(url_for("get_categories"))

            return render_template("add_category.html")
        else:
            # display 403 error page
            flash("You have tried to access an IT user only page.")
            return render_template("403.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # ituser only access
        if session["user"] == "ituser":
            if request.method == "POST":
                submit_route_category = {
                    "category_name": request.form.get("category_name")
                }
                mongo.db.categories.update({"_id": ObjectId(category_id)},
                                           submit_route_category)
                flash("Category Updated")
                return redirect(url_for("get_categories"))

            category = mongo.db.categories.find_one({"_id": ObjectId(
                                                        category_id)})
            return render_template("edit_category.html", category=category)

        else:
            # display 403 error page
            flash("You have tried to access an IT user only page.")
            return render_template("403.html")


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # ituser only access
        if session["user"] == "ituser":
            mongo.db.categories.delete_one({"_id": ObjectId(category_id)})
            flash("Category Deleted")
            return redirect(url_for("get_categories"))

        else:
            # display 403 error page
            flash("You have tried to access an IT user only page.")
            return render_template("403.html")


# cycling tip categories
@app.route("/add_cycling_tip_category", methods=["GET", "POST"])
def add_cycling_tip_category():
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # ituser only access
        if session["user"] == "ituser":
            if request.method == "POST":
                cycling_tip_category = {
                    "category_name": request.form.get("category_name")
                }
                mongo.db.cycling_tip_categories.insert_one(
                    cycling_tip_category)
                flash("New Cycling Tip Category Added")
                return redirect(url_for("get_categories"))

            return render_template("add_cycling_tip_category.html")

        else:
            # display 403 error page
            flash("You have tried to access an IT user only page.")
            return render_template("403.html")


@app.route("/edit_cycling_tip_category/<cycling_tip_category_id>",
           methods=["GET", "POST"])
def edit_cycling_tip_category(cycling_tip_category_id):
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # ituser only access
        if session["user"] == "ituser":
            if request.method == "POST":
                submit_cycling_tip_category = {
                    "category_name": request.form.get("category_name")
                }
                mongo.db.categories.update({"_id": ObjectId(
                    cycling_tip_category_id)}, submit_cycling_tip_category)
                flash("Cycling Tip Category Updated")
                return redirect(url_for("get_categories"))

            cycling_tip_category = mongo.db.cycling_tip_categories.find_one(
                {"_id": ObjectId(cycling_tip_category_id)})
            return render_template("edit_cycling_tip_category.html",
                                   cycling_tip_category=cycling_tip_category)
        else:
            # display 403 error page
            flash("You have tried to access an IT user only page.")
            return render_template("403.html")


@app.route("/delete_cycling_tip_category/<cycling_tip_category_id>")
def delete_cycling_tip_category(cycling_tip_category_id):
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # ituser only access
        if session["user"] == "ituser":
            mongo.db.cycling_tip_categories.delete_one(
                {"_id": ObjectId(cycling_tip_category_id)})
            flash("Cycling Tip Category Deleted")
            return redirect(url_for("get_categories"))
        else:
            # display 403 error page
            flash("You have tried to access an IT user only page.")
            return render_template("403.html")


# difficulty level categories
@app.route("/add_difficulty_level", methods=["GET", "POST"])
def add_difficulty_level():
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # ituser only access
        if session["user"] == "ituser":
            if request.method == "POST":
                difficulty_level = {
                    "route_difficulty": request.form.get("route_difficulty")
                }
                mongo.db.difficulty_levels.insert_one(difficulty_level)
                flash("New Difficulty Level Added")
                return redirect(url_for("get_categories"))

            return render_template("add_difficulty_level.html")
        else:
            # display 403 error page
            flash("You have tried to access an IT user only page.")
            return render_template("403.html")


@app.route("/edit_difficulty_level/<difficulty_level_id>",
           methods=["GET", "POST"])
def edit_difficulty_level(difficulty_level_id):
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # ituser only access
        if session["user"] == "ituser":
            if request.method == "POST":
                submit_difficulty_level = {
                    "route_difficulty": request.form.get("route_difficulty")
                }
                mongo.db.difficulty_levels.update({"_id": ObjectId(
                    difficulty_level_id)}, submit_difficulty_level)
                flash("Difficulty Level Updated")
                return redirect(url_for("get_categories"))

            difficulty_level = mongo.db.difficulty_levels.find_one(
                {"_id": ObjectId(difficulty_level_id)})
            return render_template("edit_difficulty_level.html",
                                   difficulty_level=difficulty_level)

        else:
            # display 403 error page
            flash("You have tried to access an IT user only page.")
            return render_template("403.html")


@app.route("/delete_difficulty_level/<difficulty_level_id>")
def delete_difficulty_level(difficulty_level_id):
    if not session.get("user"):
        flash("Please join Veloroute for full user access.")
        return render_template("403.html")
    else:
        # ituser only access
        if session["user"] == "ituser":
            mongo.db.difficulty_levels.delete_one(
                {"_id": ObjectId(difficulty_level_id)})
            flash("Difficulty Level Deleted")
            return redirect(url_for("get_categories"))

        else:
            # display 403 error page
            flash("You have tried to access an IT user only page.")
            return render_template("403.html")


# ------------------------ error handlers ---------------------------------- #
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


# ------------------------ run app ----------------------------------------- #
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
