from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from functools import wraps
import os
from dotenv import load_dotenv

from asset_utility import AssetUtility

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)

# Setup Flask Login
login_manager = LoginManager()
login_manager.init_app(app)


# Dummy User
class User(UserMixin):
    def __init__(self):
        self.id = 2
        self.username = 'seth.luan@24krat.io'
        self.user_type = 0
        self.profile_image = ''


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.user_type != 0:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    user = User()
    if user:
        return user
    else:
        return None


@app.route('/')
def home():
    assets = AssetUtility().all_assets()
    return render_template('index.html', assets=assets)


@app.route('/login')
def login():
    user = User()
    login_user(user)
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
