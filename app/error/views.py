from app.error import error
from flask import render_template


@error.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403
