from flask import Blueprint, render_template, request

extra_trees_bp = Blueprint('extra_trees_bp', __name__, url_prefix='/extra-trees')

@extra_trees_bp.route('/basic-concepts')
def basic_concepts():
    return render_template('extra_trees_basic_concepts.html')

@extra_trees_bp.route('/application', methods=['GET', 'POST'])
def application():
    prediction = None
    confidence = None
    
    if request.method == 'POST':
        # Capturamos datos del formulario
        critic_score = float(request.form['critic_score']) # Escala 0-100
        user_score = float(request.form['user_score'])     # Escala 0-10
        release_year = int(request.form['release_year'])
        
        # --- SIMULACIÓN DE EXTRA TREES CLASSIFIER ---
        # Extra Trees es un ensamble. Simulamos el voto de 100 árboles de decisión
        # usando cortes aleatorios (random splits) típicos del algoritmo Extra Trees
        
        votes_for_hit = 0
        total_trees = 100
        
        # Árboles evaluando Critic Score (pesa mucho en ventas)
        if critic_score >= 85: votes_for_hit += 40
        elif critic_score >= 70: votes_for_hit += 15
        else: votes_for_hit += 2
            
        # Árboles evaluando User Score
        if user_score >= 8.5: votes_for_hit += 30
        elif user_score >= 7.0: votes_for_hit += 10
        else: votes_for_hit += 1
            
        # Árboles evaluando el Año (los juegos modernos tienen mercados más grandes)
        if release_year >= 2015: votes_for_hit += 20
        elif release_year >= 2000: votes_for_hit += 10
        else: votes_for_hit += 5
            
        # Extra Trees calcula la probabilidad basada en la mayoría de votos
        probability_hit = votes_for_hit / total_trees
        
        # Threshold de clasificación: 0.5
        if probability_hit >= 0.5:
            prediction = 'HIGH SALES (Commercial Hit)'
            confidence = probability_hit * 100
        else:
            prediction = 'LOW/MEDIUM SALES'
            confidence = (1 - probability_hit) * 100
            
        # Evitar 100% perfecto para mayor realismo
        confidence = min(max(confidence, 51.2), 98.7)
            
        return render_template('extra_trees_application.html', 
                             prediction=prediction, 
                             confidence=round(confidence, 1))
                             
    return render_template('extra_trees_application.html')
