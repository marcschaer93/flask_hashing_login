from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    """Form for registering a user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])
    email = EmailField("E-Mail", validators=[InputRequired(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Form for registering a user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])


class UserForm(FlaskForm):
    """Form showing details of a user"""
        
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])
    email = EmailField("E-Mail", validators=[InputRequired(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])

class FeedbackForm(FlaskForm):
    """Form for a new Feedback"""

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])
    
