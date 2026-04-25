from flask import Blueprint, render_template

linear_regression_bp = Blueprint('linear_regression_bp', __name__, url_prefix='/linear-regression')

@linear_regression_bp.route('/basic-concepts')
def basic_concepts():
    return render_template('linear_basic_concepts.html')

@linear_regression_bp.route('/application')
def application():
    return render_template('linear_application.html')
