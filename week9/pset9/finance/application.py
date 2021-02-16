import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    buys = db.execute(
        "SELECT symbol, name, SUM(CASE WHEN type='buy' THEN shares WHEN type='sell' THEN -shares END) as 'shares' FROM purchase_track WHERE user_id = ? GROUP BY symbol", session['user_id'])

    total = 0
    for row in buys:
        symbol = row['symbol']
        result = lookup(symbol)
        row['price'] = result['price']
        row['total'] = row['price'] * row['shares']
        total += row['total']

    return render_template("stocks.html", rows=buys, total=(10000 - total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == 'GET':
        return render_template("buy.html")

    if request.method == 'POST':
        symbol = request.form.get('symbol')

        if not symbol:
            return apology('must provide a symbol', 400)

        if not request.form.get('shares'):
            return apology('must provide a shares', 400)

        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("must provide shares as a positive integer", 400)

        if shares < 1:
            return apology('must provide a positive integer', 400)

        response = lookup(symbol)

        if response is None:
            return apology('symbol does not exist', 400)

        priceShare = float(response['price'])

        userCash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = userCash[0]['cash']

        total = priceShare * shares

        if cash < total:
            return apology("You can't affort!", 400)
        else:
            db.execute("INSERT INTO purchase_track (user_id, symbol, name, shares, price, date, type) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       session["user_id"], response['symbol'], response['name'], shares, priceShare, datetime.today().strftime("%d/%m/%Y %H:%M:%S"), 'buy')
            db.execute("UPDATE users SET cash = ? WHERE id = ?", (cash-total), session["user_id"])

        flash('Bought!')
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    histories = db.execute("SELECT symbol, shares, price, date, type FROM purchase_track")
    return render_template("history.html", histories=histories)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":

        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide a symbol", 400)

        response = lookup(symbol)

        if response is None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", response=response)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        name = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not name:
            return apology("must provide username", 400)

        username = name.strip()

        if not password:
            return apology("must provide a password", 400)

        if len(password) < 8:
            return apology('Make sure your password is at lest 8 letters', 400)
        elif re.search('[0-9]', password) is None:
            return apology('Make sure your password has a number in it', 400)
        elif re.search('[A-Z]', password) is None:
            return apology('Make sure your password has a capital letter in it', 400)

        if password != confirmation:
            return apology("passwords do not match", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) == 1:
            return apology("that username already exists", 400)

        user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username,
                             generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

        session["user_id"] = user_id
        flash('Successfully registered')
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    symbols = db.execute("SELECT symbol FROM purchase_track WHERE user_id = ? GROUP BY symbol", session['user_id'])

    if request.method == 'GET':
        if not symbols:
            return apology("You have no shares to sell, try to buy some first!", 400)
        else:
            return render_template("sell.html", symbols=symbols)

    if request.method == 'POST':

        symbol = request.form.get('symbol')
        shares = int(request.form.get('shares'))

        if not symbols:
            return apology("You have no shares to sell, try to buy some first!", 400)

        if not symbol:
            return apology("You must select a symbol", 400)

        if shares < 1:
            return apology("must provide a positive integer", 400)

        sharesDB = db.execute(
            'SELECT shares FROM purchase_track WHERE user_id = ? AND symbol = ? GROUP BY symbol', session['user_id'], symbol)

        if shares > sharesDB[0]['shares']:
            return apology("You don't have this many shares of the stock", 400)

        response = lookup(symbol)
        priceSell = float(response['price'])

        userCash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = userCash[0]['cash']

        total = priceSell * shares

        db.execute("INSERT INTO purchase_track (user_id, symbol, name, shares, price, date, type) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], response['symbol'], response['name'], shares, priceSell, datetime.today().strftime("%d/%m/%Y %H:%M:%S"), 'sell')
        db.execute("UPDATE users SET cash = ? WHERE id = ?", (cash + total), session["user_id"])

        flash('Sold!')
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
