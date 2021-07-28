from flask import render_template, redirect, request, session, g
import requests
from requests.api import post
from models import *
from app import app, db
from werkzeug.security import check_password_hash, generate_password_hash

# if user is signed in, get username from session and assign to g.username
@app.before_request
def get_user_session():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if user:
        g.username = user.username
        g.user_id = user.id
    else:
        g.username = None
        g.user_id = None

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
        elif User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
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
        if not user or not check_password_hash(user.password, password):
            return render_template('signin.html', message = "Invalid email or password")
        else:
            session.clear()
            session["user_id"] = user.id
            return redirect('/')

# sign out user
@app.route('/signout')
def sign_out():
    session.clear()
    return redirect('/')

# GET - show threads in forums, POST - post new thread to forum
@app.route('/forums/<forum_id>', methods=["GET","POST"])
def show_forum(forum_id):
    if request.method == "GET":
        forum = Forum.query.get(forum_id)
        threads = Thread.query.filter_by(forum_id=forum_id).order_by(Thread.last_reply.desc()).all()
        return render_template('forum.html',forum=forum, threads=threads)
    if request.method == "POST":
        if g.user_id:
            title = request.form["title"]
            content = request.form["content"]
            new_thread = Thread(forum_id, title, g.user_id, content)
            db.session.add(new_thread)
            db.session.commit()
            return redirect(f'/threads/{new_thread.id}')
        else:
            return redirect('/')


# GET - show a thread and its posts
@app.route('/threads/<thread_id>', methods=["GET","POST"])
def show_thread(thread_id):
    if request.method == "GET":
        thread = Thread.query.get(thread_id)
        parent = thread.forum
        posts = Post.query.filter_by(thread_id=thread_id).order_by(Post.created_at.desc()).all()
        return render_template('thread.html',posts=posts,thread=thread,parent=parent)
    if request.method == "POST":
        if g.user_id:
            content = request.form["content"]
            new_post = Post(thread_id, g.user_id, content)
            db.session.add(new_post)
            db.session.commit()
        return redirect(f'/threads/{thread_id}')

@app.route('/threads/<thread_id>/edit', methods=["POST"])
def edit_thread(thread_id):
    thread = Thread.query.get(thread_id)
    if g.user_id == thread.user_id:
        thread.title = request.form["title"]
        thread.content = request.form["content"]
        thread.edited_at = datetime.datetime.now()
        db.session.commit()
    return redirect(f'/threads/{thread_id}')

@app.route('/threads/<thread_id>/delete')
def delete_thread(thread_id):
    thread = Thread.query.get(thread_id)
    if g.user_id == thread.user_id:
        for post in thread.posts:
            db.session.delete(post)
        db.session.commit()
        db.session.delete(thread)
        db.session.commit()
    return redirect(f'/forums/{thread.forum_id}')