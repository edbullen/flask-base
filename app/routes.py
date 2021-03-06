from flask import render_template, flash, redirect, url_for
from flask import request
from werkzeug.urls import url_parse
from app import app
from app import db

from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import EditProfileForm
from app.forms import PostForm  #unused?
from app.forms import ResetPasswordRequestForm
from app.forms import ResetPasswordForm
from app.email import send_password_reset_email
from app.forms import AddAppData

from flask_login import current_user, login_user
from flask_login import login_required
from flask_login import logout_user

from sqlalchemy.exc import IntegrityError

# Change to add confirm functionality for deletes etc 2019-01-08
from functools import wraps
from urllib.parse import urlencode, quote, unquote

from app.models import User
from app.models import AppData
#from app.models import Post

from datetime import datetime

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():

    return render_template('index.html', title = "Home",form=None )

# Change to add confirm functionality for deletes etc 2019-01-08
def confirmation_required(desc_fn):
    def inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.args.get('confirm') != '1':
                desc = desc_fn()
                return redirect(url_for('confirm',
                    desc=desc, action_url=quote(request.url)))
            return f(*args, **kwargs)
        return wrapper
    return inner


@app.before_request
def before_request():
    if current_user.is_authenticated: 
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        #This section ensures a non-Authorised user can't progress beyond the main index
        if current_user.isAuth == 0 and current_user.isSuper == 0:
            if request.path != url_for('index') and request.path != url_for('logout') :
                return redirect(url_for('index'))

# Change to add confirm functionality for deletes etc 2019-01-08
@app.route('/confirm')
def confirm():
    desc = request.args['desc']
    action_url = unquote(request.args['action_url'])
    mtext = action_url.split("/")
    # Assumes URL is in format Action / Item
    message = mtext[-2].replace("_"," ") + " " + mtext[-1]

    return render_template('confirm.html', desc=desc, action_url=action_url, message=message.capitalize())
# Change to add confirm functionality for deletes etc 2019-01-08
def you_sure():
    return "Confirm Action"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
       user = User.query.filter_by(username=form.username.data).first()
       if user is None or not user.check_password(form.password.data):
           flash('Invalid username or password')
           return redirect(url_for('login'))
       login_user(user, remember=form.remember_me.data)
       next_page = request.args.get('next')
       if not next_page or url_parse(next_page).netloc != '':
           next_page = url_for('index')
       return redirect(next_page)
    return render_template('login.html', title='Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    datestring = datetime.strftime(user.last_seen, "%A %d %b %Y at %H:%M UTC")
    page = request.args.get('page', 1, type=int)
    return render_template('user.html', user=user, datestring=datestring)

@app.route('/edit_profile/<username>', methods=['GET','POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EditProfileForm(user.username)
    boolmapper = {False:0, True:1}    #Map boolean back to 1/0 to store in database
    isauthOrig = user.isAuth          # bug-fix for non-Admin user editing profile - don't reset this flag

    # if we are editing someone else's profile, need to bounce them to the /index
    if current_user.username != username and (current_user.isAdmin != 1 and current_user.isSuper != 1):
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user.username = form.username.data
        user.about_me = form.about_me.data
        user.email = form.email.data
        datestring = datetime.strftime(user.last_seen, "%A %d %b %Y at %H:%M UTC")
        user.isAdmin = boolmapper[form.isadmin.data]
        if current_user.isAdmin == 1 or current_user.isSuper:
            user.isAuth = boolmapper[form.isauth.data]
        else:
            user.isAuth = isauthOrig
        db.session.commit()
        flash('Your changes have been saved.')
        #return redirect(url_for('edit_profile', username = user.username))
        return render_template('user.html', user=user, datestring=datestring)
    elif request.method == 'GET':
        form.username.data = user.username
        form.about_me.data = user.about_me
        form.email.data = user.email
        #if (user.isAdmin == 1) or (user.isSuper == 1):
        form.isadmin.data = user.isAdmin
        form.isauth.data = user.isAuth
        return render_template('edit_profile.html', title='Edit Profile', form=form)
    return render_template('edit_profile.html', title='Edit Profile', form=form)

# Change to allow deletion of users - 2019-01-08
@app.route('/delete_user/<username>', methods=['GET','POST'])
@login_required
@confirmation_required(you_sure)
def delete_user(username):
    user = User.query.filter_by(username = username).first_or_404()
    datestring = datetime.strftime(user.last_seen, "%A %d %b %Y at %H:%M UTC")
    confirmed = request.args.get('confirm')
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.isAdmin == 1 or current_user.isSuper:
        db.session.delete(user)
        db.session.commit()
        flash('Deleted User' + username)

    #return render_template('users.html')
    return redirect(url_for('users'))

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/users')
@login_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.username.desc()).paginate(
                   page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('users', page=users.next_num) \
        if users.has_next else None
    prev_url = url_for('users', page=users.prev_num) \
        if users.has_prev else None

    return render_template("users.html", title='Users',
                            users=users.items, next_url=next_url,prev_url=prev_url)


@app.route('/add_app_data', methods=['GET', 'POST'])
@login_required
def add_app_data():
    form = AddAppData()
    appData = AppData() # db model imported from models.py
    if form.validate_on_submit():
        appData.item = form.item.data
        appData.description = form.description.data
        appData.value = form.value.data

        db.session.add(appData)
        try:
            db.session.commit()
        except IntegrityError as err:
            flash('ERROR: Data Integrity/Duplicate Error - changes NOT saved.')
            db.session.rollback()
            return redirect(url_for('index'))
        flash('Your changes have been saved.')
        # return redirect(url_for('edit_profile', username = user.username))
        return redirect(url_for('index'))
    return render_template('app_data.html', title='Add Data', form=form)


"""
@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template("index.html", title='Explore',
                            posts=posts.items, next_url=next_url,prev_url=prev_url)

"""