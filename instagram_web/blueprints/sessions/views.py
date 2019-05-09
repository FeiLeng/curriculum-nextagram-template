from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from models.user import User
from werkzeug.security import check_password_hash
from app import login_manager
from flask_login import login_user, logout_user,current_user


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')



@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route("/signin", methods=['POST'])
def create():
    username = request.form['username']
    user = User.get_or_none(User.username == username)

    if not user:
        flash(f'User not found with username:{username}')
        return render_template('sessions/new.html')

    # password keyed in by the user in the sign in form
    password_to_check = request.form['password']
    # password hash stored in database for a specific user
    hashed_password = user.password

    if not check_password_hash(hashed_password, password_to_check):
        flash(f'Incorrect password for username:{username}')
        return render_template('sessions/new.html')

    session["username"] = username

    login_user(user, force=True)
    flash(f'Congratulations {username}, you have successfully signed in.') # Set the sessions if the user has entered correct password & username
    return redirect(url_for('sessions.new')) # Redirect the logged in user somewhere


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@sessions_blueprint.route("/logout")
def destroy():
    logout_user()
    return redirect(url_for('sessions.new'))

# @sessions_blueprint.route("/loggedin")
# def test():
#     return render_template('sessions/test.html')

@sessions_blueprint.route('/', methods=['POST'])
def create1():
    pass


@sessions_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@sessions_blueprint.route('/', methods=["GET"])
def index():
    pass


@sessions_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@sessions_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
