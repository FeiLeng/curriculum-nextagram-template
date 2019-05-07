from app import app
from flask import Flask, render_template, request, redirect, url_for
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(users_blueprint, url_prefix="/users")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')

# @app.route("/new")
# def signup():
#     return render_template('users.new.html')


if __name__ == '__main__':
   app.run()

