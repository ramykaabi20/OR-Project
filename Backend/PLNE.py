from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from gurobipy import Model, GRB, quicksum

app = Flask(__name__)
CORS(app)

def solve_tsp(distances):
    n = len(distances)
    
    # Créer le modèle
    model = Model("TSP")
    
    # Variables de décision
    x = model.addVars(n, n, vtype=GRB.BINARY, name="x")
    u = model.addVars(n, vtype=GRB.INTEGER, name="u")
    
    # Fonction objectif
    model.setObjective(quicksum(distances[i][j] * x[i,j] for i in range(n) for j in range(n)), GRB.MINIMIZE)
    
    # Contraintes
    # Chaque ville doit être visitée une seule fois (entrée)
    for j in range(n):
        model.addConstr(quicksum(x[i,j] for i in range(n) if i != j) == 1)
    
    # Chaque ville doit être quittée une seule fois (sortie)
    for i in range(n):
        model.addConstr(quicksum(x[i,j] for j in range(n) if i != j) == 1)
    
    # Élimination des sous-tours (MTZ formulation)
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                model.addConstr(u[i] - u[j] + n * x[i,j] <= n - 1)
    
    # Fixer u[0] à 0 (ville de départ)
    model.addConstr(u[0] == 0)
    
    # Bornes pour les variables u
    for i in range(1, n):
        model.addConstr(u[i] >= 1)
        model.addConstr(u[i] <= n - 1)
    
    # Optimisation
    model.optimize()
    
    # Récupération de la solution
    if model.status == GRB.OPTIMAL:
        tour = []
        current = 0  # Commencer par la ville 0
        for _ in range(n):
            for j in range(n):
                if current != j and x[current,j].x > 0.5:
                    tour.append(current)
                    current = j
                    break
        tour.append(current)  # Ajouter la dernière ville
        tour.append(0)  # Retour à la ville de départ
        
        return {
            "status": "success",
            "tour": tour,
            "total_distance": model.objVal,
            "distances": distances
        }
    else:
        return {
            "status": "error",
            "message": "Pas de solution optimale trouvée"
        }

@app.route('/api/solve-tsp', methods=['POST'])
def api_solve_tsp():
    try:
        data = request.json
        distances = data['distances']
        result = solve_tsp(distances)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
