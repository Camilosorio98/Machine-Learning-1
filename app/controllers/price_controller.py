from flask import Blueprint, render_template
from app.models.price_model import PriceModel

price_bp = Blueprint('price', __name__)
price_inst = PriceModel()

@price_bp.route('/use-cases/price')
def index():
    return render_template('cases/price.html', data=price_inst)