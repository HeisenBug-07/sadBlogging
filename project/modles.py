from project import db, loginManager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


@loginManager.user_loader
def loadUser(userId):
    return User.query.get(userId)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    passwordHash = db.Column(db.String, nullable=False)
    profilePic = db.Column(db.String, nullable=False, default='pic1.jpg')
    profileBg = db.Column(db.String, nullable=False, default='profilebg.jpg')
    bio = db.Column(db.String, nullable=False, default='fill bio here')
    posts = db.relationship('Post', backref='user', lazy=True)

    def __init__(self, userName, email, password):
        self.userName = userName
        self.email = email
        self.passwordHash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    postImage = db.Column(db.String, nullable=True, default='defaultPic1.png')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content, postImage, userId):
        self.title = title
        self.content = content
        self.postImage = postImage
        self.userId = userId
