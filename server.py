from flask import (Flask, render_template, request, redirect, url_for, flash, abort)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, connect_to_db, User, Contact, Note
from forms import LoginForm, SignupForm

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = "dev"

login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
# Endpoints/Routes
@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Logged in Succesfully.")

            next = request.args.get("next")

            if next == None or not next[0]=="/":
                next = url_for('dashboard')
            
            return redirect(next)

    return render_template('login.html', form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():

    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registered Successfully.")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for('home'))

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)