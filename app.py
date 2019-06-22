from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
from passlib.hash import sha256_crypt
from functools import wraps
import requests
import time

# create the flask app from config file and instantiate db
application = app = Flask(__name__)
app.config.from_object('config.AWSConfig')
db = SQLAlchemy(app)

# init mail client
mail = Mail()
mail.init_app(app)

# have to import since models relies on db object
from models import Cities, Users, Listings
from forms import RegisterForm, ContactForm, ProfileForm
                    

# custom decorator to verify user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash ("Please login to see this content.", "danger")
            return redirect(url_for('login'))
    return wrap

# register user with form and validating from wtforms
# if valid notify user and redirect if successful, otherwise display error
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    # use passwordrandom.com to get user ip and recommend password
    recommendation = requests.get('https://www.passwordrandom.com/query?command=password')\
        .content.decode("utf-8")
    ip = requests.get('https://www.passwordrandom.com/query?command=ip').\
        content.decode("utf-8")
    flash("We recommend using password: '%s'" % recommendation, 'warning')
    if request.method == 'POST' and form.validate():
        new_user = Users(first=form.first.data,
                         last=form.last.data,
                         email=form.email.data,
                         username=form.username.data,
                         city=form.city.data,
                         password=sha256_crypt.encrypt(str(form.password.data)),
                         ip=ip,
                         register_date=time.strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(new_user)
        db.session.commit()
        session.pop('_flashes', None)
        flash('Welcome to flippin!\nYour account has been successfully created.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

# homepage
@app.route('/')
def index():
    return render_template('home.html')

# login user. does not use wtforms since little validation needs to be done.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get user information and query database for match
        username = request.form['username']
        password_candidate = request.form['password']
        result = Users.query.filter_by(username=username).first()

        # if info is correct redirect and set session variables
        if result is not None:
            password = result.password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                session['city'] = result.city
                # gets the related city name given the users relevant foreign key
                session['city_name'] = Cities.query.filter_by(id=result.city).first().name
                flash('Log in successful. Enjoy!', 'success')
                return redirect(url_for('items'))

            # otherwise return relevant error
            else:
                return render_template('login.html', error="Invalid password")
        else:
            return render_template('login.html', error="No user found")

    return render_template('login.html')

# items page, requires that user is logged in
@app.route('/items')
@is_logged_in
def items():
    listings = Listings.query.filter_by(city=session['city']).all()
    return render_template('items.html', items=listings, length=len(listings))


@app.route('/profile', methods=['GET', 'POST'])
@is_logged_in
def profile():
    form = ProfileForm(request.form)
    user = Users.query.filter_by(username=session['username']).first()
    if request.method == 'POST' and form.validate():
        user.email = form.email.data
        user.city = form.city.data
        user.password = sha256_crypt.encrypt(str(form.password.data))
        session['city'] = form.city.data
        db.session.commit()
        flash('Your account settings have been updated.', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user, form=form)


@app.route('/delete')
@is_logged_in
def delete_user():
    db.session.query(Users).filter(Users.username == session['username']).delete()
    db.session.commit()
    session.clear()
    flash('Your account has been deleted! Sorry to see you go.', 'success')
    return render_template('home.html')

# logout method, clear session variables and redirect
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    # on submit send email with form contents to and from support email
    if request.method == 'POST' and form.validate():
        # don't need to specify sender, default is in app config
        msg = Message(form.subject.data, sender="support@flippinapp.com",
                      recipients=["support@flippinapp.com"])
        msg.body = """
        From: %s <%s>
        About: %s
        
        %s
        """ % (form.name.data, form.email.data, form.subject.data, form.message.data)
        mail.send(msg)
        flash('Thanks for reaching out! We will get back to you shortly.', 'success')
    return render_template('contact.html', form=form)


if __name__ == '__main__':
    app.run()
