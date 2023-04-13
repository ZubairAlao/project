import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///helpdesk.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show complaints table"""
    if "user_id" not in session:
        return redirect("/login")

    # query database for current user
    complaints = db.execute("SELECT c.subject, c.description, c.created_at, r.message, c.id as complaint_id, u.username, u.id as user_id FROM complaints c LEFT JOIN replies r ON c.id = r.complaint_id LEFT JOIN users u ON c.user_id = u.id WHERE c.user_id = :user_id ORDER BY c.created_at DESC", user_id=session["user_id"])
    # complaints = db.execute("SELECT subject, description, created_at FROM complaints AND message FROM replies WHERE user_id = :user_id", user_id=session["user_id"])

    """Show user profile"""
    # Retrieve user information from the database
    user_info = db.execute("SELECT username FROM users WHERE id = :user_id", user_id=session["user_id"])

    return render_template("index.html", complaints=complaints, username=user_info[0]["username"])


@app.route("/open")
@login_required
def open():
    """Show open table"""
    if "user_id" not in session:
        return redirect("/login")

    # query database for current user

    complaints = db.execute("SELECT c.subject, c.description, c.created_at, r.message, c.id as complaint_id, u.username, u.id as user_id FROM complaints c LEFT JOIN replies r ON c.id = r.complaint_id LEFT JOIN users u ON c.user_id = u.id WHERE c.user_id = :user_id ORDER BY c.created_at DESC", user_id=session["user_id"])
    # complaints = db.execute("SELECT subject, description, created_at FROM complaints AND message FROM replies WHERE user_id = :user_id", user_id=session["user_id"])

    """Show reply messages"""
    # Retrieve user information from the database
    user_info = db.execute("SELECT username FROM users WHERE id = :user_id", user_id=session["user_id"])

    return render_template("open.html", complaints=complaints, username=user_info[0]["username"])


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
        session["is_admin"] = rows[0]["is_admin"]

        # Redirect user to home page
        if session["is_admin"]:
            return redirect("/admin")
        else:
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


@app.route("/complaints", methods=["GET", "POST"])
def complaints():
    """Make complaints"""
    if request.method == 'POST':
        subject = request.form.get("subject")
        description = request.form.get("description")

        if not subject:
            return apology("invalid subject title", 400)
        elif not description:
            return apology("enter description", 400)
        else:
            # Insert the complaint into the database
            db.execute("INSERT INTO complaints (user_id, subject, description) VALUES (?, ?, ?)",
                       session["user_id"], subject, description)
            return redirect('/')
    else:
        # Render the complaints form
        return render_template("complaints.html")


@app.route("/reply", methods=["GET", "POST"])
@login_required
def reply():
    """answer complaints"""
    message = request.form.get("message")
    complaint_id = request.form.get("complaint_id")

    # insert into message with a foreign relationship to complaint.id
    db.execute("INSERT INTO replies (message, complaint_id, user_id) VALUES (?, ?, ?)", message, complaint_id, session["user_id"])

    # pass retrived row to the template for the next page
    return redirect("/admin")


@app.route("/admin")
@login_required
def admin():

    """Show admin table"""
     # Ensure user is an admin
    if not session.get("is_admin"):
        flash("You must be an admin to access this page.", "error")
        return redirect("/")

    # retrieve all users from the database
    complaints = db.execute("SELECT complaints.id as complaint_id, users.id as user_id, users.username, users.hash, users.is_admin, complaints.subject, complaints.description, complaints.created_at, replies.id as reply_id, replies.message, replies.created_at as reply_created_at FROM complaints JOIN users ON complaints.user_id = users.id LEFT JOIN replies ON complaints.id = replies.complaint_id ORDER BY reply_id IS NULL DESC, reply_created_at DESC;")

    """Show user profile"""
    # Retrieve user information from the database
    user_info = db.execute("SELECT username FROM users WHERE id = :user_id", user_id=session["user_id"])

    return render_template("admin.html", complaints=complaints, username=user_info[0]["username"])


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Signup user"""
    if request.method == 'POST':

        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")

        if not username:
            return apology("invalid username", 400)
        elif not password:
            return apology("enter password", 400)
        elif password != confirmPassword:
            return apology("The passwords do not match", 400)

        # generate a password hash
        password_hash = generate_password_hash(password)

        try:
            # add user to database database
            new_user_id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                    username=username, hash=password_hash)
        except:
            # username exist
            return apology("username already exists", 400)

        # remember to keep track of user that is login
        session["user_id"] = new_user_id

        return redirect('/login')
        # # Redirect user to home page
        # return redirect(url_for("index"))

    else:
        # get
        return render_template('signup.html')

@app.route("/about")
def about():
    """About"""
    return render_template("about.html")


@app.route("/deletecomplaint", methods=["POST"])
def deletecomplaint():
    complaint_id = request.form.get("complaint_id")
    if complaint_id:
        user_id = session["user_id"]
        db.execute("DELETE FROM complaints WHERE id = ? AND user_id = ?", complaint_id, user_id)
    return redirect('/')


@app.route("/deleteadmin", methods=["POST"])
def deleteadmin():
    reply_id = request.form.get("reply_id")
    if reply_id:
        db.execute("DELETE FROM replies WHERE id = ?", reply_id)
    return redirect('/admin')