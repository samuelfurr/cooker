from flask import render_template
from cooker import cooker, db

@cooker.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@cooker.errorhandler(500)
def not_found_error(error):
    return render_template('500.html'), 500
