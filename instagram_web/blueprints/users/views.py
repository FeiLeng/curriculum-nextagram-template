from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import user
from werkzeug.security import generate_password_hash


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')



@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

@users_blueprint.route("/signup_form", methods=['POST'])
def signup_form():
    hashed_password = generate_password_hash(request.args['password'])
    s = user.User(username=request.args['username'], email=request.args['email'], password=hashed_password)

    if s.save():
        flash("Successfully saved")
        return redirect(url_for('users.new'))
    else: 
        return render_template('users.new.html', username=request.args['username'], email=request.args['email'], password=request.args['password'])



@users_blueprint.route('/', methods=['POST'])
def create():
    pass


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    user_array=[]
    for person in user.User:
        user_array.append(person.username)
    return render_template('users/user.html',username=user_array)


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
