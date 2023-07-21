"""Flask App"""
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Feedback, db, connect_db 
from forms import RegisterForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
# from flask_cors import CORS
app = Flask(__name__)
 # This will enable CORS for all routes of your app.
# CORS(app)
# Add a DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hashing_login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "hyptokrypo"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
connect_db(app)

with app.app_context():
    db.create_all()

##############----- ROUTES -----####################################
####################################################################
@app.route('/')
def home():
    """Home"""
    if "username" not in session:
        flash('Please Login first!', 'danger')
        return redirect('/login')
    else:   
        return render_template('home.html')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """User registration"""
    form = RegisterForm()
    if form.validate_on_submit():
        user_data = {key: value for key, value in form.data.items() if key != 'csrf_token'}
        new_user = User.register(**user_data)

        """Longer but maybe more trustful"""
        # if form.validate_on_submit():
            # username = form.username.data
            # password = form.password.data
            # first_name = form.first_name.data
            # last_name = form.last_name.data
            # email = form.email.data
            # new_user = User.register(username, password, first_name, last_name, email)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another')
            return redirect('/login')
        session['username'] = new_user.username
        flash('Registration was successfully', 'success')
        return redirect('/')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Login Form for a user who is already registred
    if logged In save "Username" data to session
    """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.login(username, password)
        if user:
            flash('Successfully logged In!', 'success')
            session['username'] = username
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ['Invalid Password/Username!']
            flash("Password or Username doesn't match", 'danger')
        
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    """Logout a User and remove "username" data in session"""
    session.pop('username')
    flash('Goodbye!', 'primary')
    return redirect('/')

@app.route('/users/<username>')
def show_user(username):
    """Show more details about a User"""
    if "username" not in session or username != session['username']:
        flash('Please Login first!', 'danger')
        return redirect('/login')

    user = User.query.get(username)
    feedbacks = Feedback.query.all()    
    return render_template('user.html', user=user, feedbacks=feedbacks)

@app.route('/users/<username>/delete', methods=["GET", "POST"])
def delete_user(username):
    """Deletes a User completly togetehr with all self created Feedbacks"""
    if "username" not in session or username != session['username']:
        flash('Please Login first!', 'danger')
        return redirect('/login')
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    flash('User deleted', 'info')
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def feedback(username):
    """Shows a Form to create and submit a new Feedback"""
    if "username" not in session or username != session['username']:
        flash('Please Login first!', 'danger')
        return redirect('/login')
    
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash('New Feedback added', 'success')
        return redirect(f"/users/{username}")
    else:
        return render_template('new_feedback.html', form=form)

@app.route('/feedback/<int:id>/delete', methods=["GET", "POST"])
def delete_feedback(id):
    """Delets a Feedback. Only possible if its your own Feedback"""
    
    feedback = Feedback.query.get_or_404(id)
    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback removed!', 'info')
    return redirect(f"/users/{session['username']}")

@app.route('/feedback/<int:id>/update', methods=["GET", "POST"])
def update_feedback(id):
    """Update a Feedback. Only possible if its your own Feedback"""
    feedback = Feedback.query.get_or_404(id)
    
    if "username" not in session or feedback.username != session['username']:
        flash('Please Login first!', 'danger')
        return redirect('/login')

    form = FeedbackForm(obj=feedback)
    
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        # return redirect(f"/users/{feedback.username}")
        return redirect('/feedbacks')
        
    return render_template("edit_feedback.html", form=form, feedback=feedback)

@app.route('/feedbacks')
def show_all_feedbacks():
    """Shows all Feedbacks"""
    feedbacks = Feedback.query.all()
    return render_template('feedbacks.html', feedbacks=feedbacks)

    
    
    
    
        
    

