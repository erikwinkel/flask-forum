from os import name
from app import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String)
    threads = db.relationship('Thread', backref='user')
    posts = db.relationship('Post', backref='user')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return self.username

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable = False)
    title = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    content = db.Column(db.Text, nullable = False)
    posts = db.relationship('Post', backref='thread')
    created_at = db.Column(db.DateTime, nullable=False)
    edited_at = db.Column(db.DateTime)
    last_reply = db.Column(db.DateTime)

    def __init__(self, forum_id, title, user_id, content):
        self.forum_id = forum_id
        self.title = title
        self.user_id = user_id
        self.content = content
        self.created_at = datetime.datetime.now()
        self.last_reply = self.created_at

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable=False)
    edited_at = db.Column(db.DateTime)

    def __init__(self, thread_id, user_id, content):
        self.thread_id = thread_id
        self.user_id = user_id
        self.content = content
        self.created_at = datetime.datetime.now()

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    threads = db.relationship('Thread', backref='forum')

    def __init__(self, name, description):
        self.name = name
        self.description = description