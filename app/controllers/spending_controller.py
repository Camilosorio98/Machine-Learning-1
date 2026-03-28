from flask import Blueprint, render_template
from app.models.spending_model import SpendingModel

spending_bp = Blueprint('spending', __name__)
spending_inst = SpendingModel()

@spending_bp.route('/use-cases/spending')
def index():
    return render_template('cases/spending.html', data=spending_inst)