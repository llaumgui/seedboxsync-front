from flask import current_app, Blueprint, render_template, flash

# Create a Blueprint named 'root'
bp = Blueprint('root', __name__)

@bp.route('/')
@bp.route('/homepage')
def homepage():
    if current_app.config.get('INIT_ERROR'):
        flash(current_app.config['INIT_ERROR'], 'error')

    return render_template('homepage.html')
