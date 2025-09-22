# Import Flask and Blueprint
from flask import Blueprint, render_template

# Create a Blueprint named 'homepage'
bp = Blueprint('homepage', __name__)

@bp.route('/', methods=['GET'])
def register():

    return render_template('homepage.html')
