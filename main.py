from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from functools import wraps
import os
from dotenv import load_dotenv
from collectible_utility import CollectibleUtility
from user_utility import UserUtility
from forms import LoginForm

# Load env variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)

# Setup Flask Login
login_manager = LoginManager()
login_manager.init_app(app)


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.user_type != 0:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    user = user_utility.find_user(int(user_id))
    return user


collectible_utility = CollectibleUtility()
user_utility = UserUtility()


@app.route('/')
def home():
    collectible_utility.all_collectibles()
    collectibles = collectible_utility.collectibles
    return render_template('index.html', collectibles=collectibles)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.user_name.data
        password = form.password.data
        for user in user_utility.users.values():
            if user.user_name == username:
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    flash("Please check your password and try again.")
                    return redirect(url_for("login"))
        flash("User doesn't exist. Please try again.")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/collectible/<int:collectible_id>')
def collectible_detail(collectible_id):
    collectible = collectible_utility.find_collectible(collectible_id)
    return render_template('collectible.html', collectible=collectible)


@app.route('/buy/<int:collectible_id>')
def buy(collectible_id):
    if not current_user.is_authenticated:
        flash("Please login first!")
        return redirect(url_for('collectible_detail', collectible_id=collectible_id))
    else:
        collectible_utility.assign_owner(collectible_id, current_user.id)
        return redirect(url_for('my_collection'))


@app.route('/my_collection')
def my_collection():
    collections = collectible_utility.find_collectible_by_user(current_user.id)
    return render_template('my_collections.html', collections=collections)


@app.route('/marketplace')
def marketplace():
    collectibles = collectible_utility.collectibles_on_marketplace()
    return render_template('marketplace.html', collectibles=collectibles)


@app.route('/list_on_marketplace/<int:collectible_id>')
@login_required
def list_on_marketplace(collectible_id):
    collectible_utility.list_on_marketplace(collectible_id)
    flash("Listed on marketplace!")
    return redirect(url_for('my_collection'))


@app.route('/unlist_from_marketplace/<int:collectible_id>')
@login_required
def unlist_from_marketplace(collectible_id):
    collectible_utility.unlist_from_marketplace(collectible_id)
    flash("Unlisted from marketplace!")
    return redirect(url_for('my_collection'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
