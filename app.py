"""Flask App"""
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
# from models import db, connect_db 
# from flask_cors import CORS

# Create a FLASK instance
app = Flask(__name__)
 # This will enable CORS for all routes of your app.
# CORS(app)
# Add a DATABASE
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# SECRET KEY
app.config['SECRET_KEY'] = "hyptokrypo"
# DEBUG TOOLBAR
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# initializes the Flask Debug Toolbar
debug = DebugToolbarExtension(app)
# connect to DATABASE
# connect_db(app)

# with app.app_context():
#     db.drop_all()
#     db.create_all()
    # db.session.add_all([c1, c2])
    # db.session.commit()

#----- ROUTES -----#