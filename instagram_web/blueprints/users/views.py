from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from werkzeug.security import generate_password_hash
from flask_login import current_user
from werkzeug import secure_filename
from instagram_web.util.helpers import *
from config import S3_BUCKET

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@users_blueprint.route("/", methods=["POST"])
def upload_file():

    if "user_file" not in request.files:
        flash("No file chosen")
        return redirect(url_for('users.profile'))
    
    file    = request.files["user_file"]

    if file.filename == "":
        return "Please select a file"

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output   	  = upload_file_to_s3(file, S3_BUCKET)
        return str(output)

    else:
        return redirect("/")


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

@users_blueprint.route("/signup_form", methods=['POST'])
def create():
    hashed_password = generate_password_hash(request.form['password'])
    s = User(username=request.form['username'], email=request.form['email'], password=hashed_password)

    if s.save():
        flash("Successfully saved")
        return redirect(url_for('users.new'))
    else: 
        return render_template('users/new.html', username=request.form['username'], email=request.form['email'], password=request.form['password'])




@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_or_none(User.id == id)
    if user:
        return render_template('users/setting.html')

    else:
        flash("invalid request")
        return redirect(url_for('home'))

@users_blueprint.route('/<username_id>', methods=["POST"])
def update(username_id):
    user = User.get_or_none(User.id == username_id)
    if user and current_user ==  user: # current_user method is from Flask-Login
        update = User.update(username=request.form['username'],email=request.form['email']).where(User.id == username_id)
        if update.execute():
            flash('You have successfully updated your details.')
#         if current_user.role != 'admin':
#  raise Exception('Unauthorized to perform this action')
        return redirect(url_for('home'))

@users_blueprint.route('/profile', methods=["get"])
def profile():
    return render_template('users/profile_form.html')


# @users_blueprint.route('/', methods=["GET"])
# def index():
#     user_array=[]
#     for person in user.User:
#         user_array.append(person.username)
#     return render_template('users/user.html',username=user_array)

# @users_blueprint.route('/', methods=['POST'])
# def create():
#     pass

# @users_blueprint.route('/<id>/edit', methods=['GET'])
# def edit(id):
#     pass


# @users_blueprint.route('/<id>', methods=['POST'])
# def update(id):
#     pass
