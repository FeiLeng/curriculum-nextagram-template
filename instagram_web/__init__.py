from app import app
from flask import Flask, render_template, request, redirect, url_for
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User


assets = Environment(app)
assets.register(bundles)

app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(images_blueprint, url_prefix="/images")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def home():
    return redirect(url_for('index'))

@app.route('/', methods=["GET"])
def index():
    user_array=[]
    for person in user.User:
        user_array.append(person.username)
    return redirect(url_for('home'), username=user_array)


if __name__ == '__main__':
   app.run()

