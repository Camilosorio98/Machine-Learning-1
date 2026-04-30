from flask import Blueprint, render_template
from app.models.Clustering import manual_kmeans_simulation, apply_clustering

clustering_bp = Blueprint('clustering_bp', __name__, url_prefix='/clustering')

@clustering_bp.route('/basic-concepts')
def basic_concepts():
    return render_template('clustering_basic_concepts.html')

@clustering_bp.route('/manual-exercise')
def manual_exercise():
    data = manual_kmeans_simulation()
    return render_template('clustering_manual_exercise.html', data=data)

@clustering_bp.route('/application')
def application():
    data = apply_clustering()
    return render_template('clustering_application.html', data=data)