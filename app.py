from flask import Flask, render_template
# Importamos cada uno de los controladores (Blueprints)
from app.controllers.sales_controller import sales_bp
from app.controllers.price_controller import price_bp
from app.controllers.spending_controller import spending_bp
from app.controllers.demand_controller import demand_bp

app = Flask(__name__, 
            template_folder='app/templates', 
            static_folder='app/static')

# --- REGISTRO DE RUTAS ---
app.register_blueprint(sales_bp)
app.register_blueprint(price_bp)
app.register_blueprint(spending_bp)
app.register_blueprint(demand_bp)

# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/linear-regression')
def linear_regression():
    return render_template('linear_regression.html')

if __name__ == "__main__":
    app.run(debug=True)