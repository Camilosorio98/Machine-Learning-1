from flask import Flask, render_template
from app.controllers.sales_controller import sales_bp
from app.controllers.price_controller import price_bp
from app.controllers.spending_controller import spending_bp
from app.controllers.demand_controller import demand_bp
from app.controllers.linear_regression_controller import linear_regression_bp
from app.controllers.logistic_regression_controller import logistic_regression_bp
from app.controllers.extra_trees_controller import extra_trees_bp  # NUEVO CONTROLADOR

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

app.register_blueprint(sales_bp)
app.register_blueprint(price_bp)
app.register_blueprint(spending_bp)
app.register_blueprint(demand_bp)
app.register_blueprint(linear_regression_bp)
app.register_blueprint(logistic_regression_bp)
app.register_blueprint(extra_trees_bp)  # NUEVO REGISTRO

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
