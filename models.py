from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model"""
    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user with hashed password and return user"""
        hashed_pwd = bcrypt.generate_password_hash(pwd)
        hashed_pwd_utf8 = hashed_pwd.decode("utf8")

        user = cls(username=username, password=hashed_pwd_utf8, email=email, first_name=first_name, last_name=last_name)

        return user 

    @classmethod
    def login(cls, username, pwd):
        """Login if password and username is correct and user already registred
        
        Return user if correct, otherwise return False
        """
        user = User.query.filter_by(username = username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            # return user instance
            return user
        else:
            return False


class Feedback(db.Model):
    """Feedback"""
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String, db.ForeignKey('users.username'))

