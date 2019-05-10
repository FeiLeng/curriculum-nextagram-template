from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from models.user import User
from models.image import Photos
from werkzeug.security import check_password_hash
from app import login_manager
from flask_login import login_user, logout_user,current_user
from werkzeug import secure_filename
from instagram_web.util.helpers import *
from config import S3_BUCKET
from playhouse.hybrid import hybrid_property

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @hybrid_property
# def profile_image_url(self):
#   return AWS_S3_DOMAIN + self.image_path


@images_blueprint.route('/uploadprofileimg', methods=["get"])
def profile():
    return render_template('images/profile_form.html')


@images_blueprint.route("/", methods=["POST"])
def upload_file():

    if "user_file" not in request.files:
        flash("No file chosen")
        return redirect(url_for('images.profile'))
    
    file    = request.files["user_file"]
    
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        image_url   	  = upload_file_to_s3(file, S3_BUCKET)
        update = User.update(profilepic=image_url).where(User.id == current_user.id)
        if update.execute():
            flash('Image uploaded')
        return redirect(url_for('images.index'))


@images_blueprint.route('/uploadphotos', methods=["GET"])
def show():
    return render_template('images/new.html')


@images_blueprint.route('/upload_photos', methods=['POST'])
def create():
    if "images" not in request.files:
        flash("No file chosen")
        return redirect(url_for(images.profile))

    file = request.files["images"]

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        image_url   	  = upload_file_to_s3(file, S3_BUCKET)
        s = Photos.create(user_id=current_user.id, images=image_url)
        if s.save():
            flash('Image uploaded')
        return redirect(url_for('images.index'))

@images_blueprint.route('/', methods=["GET"])
def index():
    photo_array=[]
    for photo in Photos.select().where(Photos.user_id==current_user.id):
        photo_array.append(photo.images)
    return render_template('users/user.html', images=photo_array)


# @images_blueprint.route('/', methods=["GET"])
# def index():
#     pass


@images_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@images_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass