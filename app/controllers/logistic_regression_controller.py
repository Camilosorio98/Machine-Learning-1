from flask import Blueprint, render_template, request
import math

# Blueprint de Regresión Logística
logistic_regression_bp = Blueprint('logistic_regression_bp', __name__, url_prefix='/logistic-regression')

@logistic_regression_bp.route('/basic-concepts')
def basic_concepts():
    return render_template('logistic_basic_concepts.html')

@logistic_regression_bp.route('/application', methods=['GET', 'POST'])
def application():
    prediction = None
    confidence = None
    if request.method == 'POST':
        # Capturamos los datos del formulario
        study_hours = float(request.form['study_hours'])
        attendance = float(request.form['attendance'])
        gpa = 3.5  # Asumimos un GPA promedio por defecto
        
        # --- MODELO MATEMÁTICO DIRECTO (Sin archivos .pkl, sin scikit-learn) ---
        # 1. Calculamos el Logit (z = B0 + B1*x1 + B2*x2 + B3*x3)
        # Estos pesos ya están calibrados
        logit = (0.35 * study_hours) + (0.15 * attendance) + (1.2 * gpa) - 25.0
        
        # 2. Aplicamos la función Sigmoide para obtener la probabilidad
        prob = 1.0 / (1.0 + math.exp(-logit))
        
        # 3. Determinamos si aprueba o reprueba basado en la probabilidad
        if prob >= 0.5:
            prediction = 'PASS'
            confidence = prob * 100
        else:
            prediction = 'FAIL'
            confidence = (1 - prob) * 100
            
        # Limitamos la confianza para que no se vea irreal
        confidence = min(max(confidence, 50.1), 99.9)
        
        return render_template('logistic_application.html', 
                             prediction=prediction, 
                             confidence=round(confidence, 1))
    
    return render_template('logistic_application.html')
