from flask import Blueprint, render_template
from app.models.demand_model import DemandModel

demand_bp = Blueprint('demand', __name__)
demand_inst = DemandModel()

@demand_bp.route('/use-cases/demand')
def index():
    return render_template('cases/demand.html', data=demand_inst)