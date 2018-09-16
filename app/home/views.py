from flask import render_template, abort, flash
from flask_login import login_required, current_user
from app.home import home


@home.route('/')
def index():
    return render_template('home/index.html', title='Home')


@home.route('/')
def homepage():
    return render_template('home/index.html', title='Home')


@home.route('/')
def dashboard():
    return render_template('home/index.html', title='Home')


@home.route('/admin/dashboard')
def admin_dashboard():
    if not current_user.is_admin:
        abort(403, description="You are not authorize to access this page.")
    return render_template('home/admin_dashboard.html',current_user=current_user, title='Dashbard')
