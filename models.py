from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    avatar = db.Column(db.String)
    threads = db.relationship('Thread', backref='user')
    posts = db.relationship('Post', backref='user')

class Thread(db.Model):
    id = db.Column(db.Integer, primay_key=True)
    title = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable = False)
    posts = db.relationship('Post', backref='thread')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable = False)
    created_at = db.Column(db.DateTime, nullable=False)
    edited_at = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable = False)

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    threads = db.relationship('Thread', backref='forum')