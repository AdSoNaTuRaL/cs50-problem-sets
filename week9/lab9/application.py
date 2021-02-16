import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))

        print(name, day, month)

        if (name and month and day) and (day in range(1, 32)) and (month in range(1, 13)):
            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        entries = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", entries=entries)

@app.route("/delete", methods=["GET"])
def delete():
    id = request.args.get("id")

    if id:
        db.execute("DELETE FROM birthdays WHERE id = ?", id)

    return redirect("/")