from flask import render_template, redirect, request, session, g
from models import *
from app import app, db
from werkzeug.security import check_password_hash, generate_password_hash

# if user is signed in, get username from session and assign to g.username
@app.before_request
def get_user_session():
    username = session.get("username")
    if username:
        g.username = username
    else:
        g.username = None

# Main page, list of all forums
@app.route('/')
def index():
    forums = Forum.query.all()
    return render_template('index.html', forums=forums)


# GET register page, form POSTs, to create new user
@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        if not username or not email or not password:
            return render_template('register.html', message = 'Error: Missing data. Please fill out all fields')
        elif User.query.filter_by(username=username) or User.query.filter_by(email=email):
            return render_template('register.html', message = "Error: An account already exists with this username or email address.")
        else:
            new_user = User(username, email, password)
            db.session.add(new_user)
            db.session.commit()
        return redirect('/signin')


# GET sign in page, form POSTs to sign in
@app.route('/signin', methods=["GET","POST"])
def sign_in():
    if request.method == "GET":
        return render_template('signin.html')
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        print(user)
        if not user or not check_password_hash(user.password, password):
            return render_template('signin.html', message = "Invalid email or password")
        else:
            session.clear()
            session["username"] = user.username
            return redirect('/')

# sign out user
@app.route('/signout')
def sign_out():
    session.clear()
    return redirect('/')