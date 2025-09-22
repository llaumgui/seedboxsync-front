# Import Flask and Blueprint
from flask import Blueprint, render_template

# Create a Blueprint named 'root'
bp = Blueprint('root', __name__)

@bp.route('/')
@bp.route('/homepage')
def homepage():

    return render_template('homepage.html')
