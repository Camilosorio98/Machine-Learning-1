from flask import Blueprint, render_template
from app.models.sales_model import SalesModel

# El nombre 'sales' debe coincidir con lo que importas en run.py
sales_bp = Blueprint('sales', __name__)
model = SalesModel()

@sales_bp.route('/use-cases/sales')
def show_sales():
 return render_template('cases/sales.html', data=model)