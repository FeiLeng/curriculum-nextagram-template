import os
import config
from flask import Flask
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')


csrf = CSRFProtect()
app = Flask('NEXTAGRAM', root_path=web_dir)
csrf.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

if __name__ == '__main__':
    app.run(debug=True)